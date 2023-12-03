import abc
import enum
import subprocess
import threading
import json
import collections
import contextlib
import os
import signal

import attr

import lfpreviewer.action as _action
from lfpreviewer.scaling import ScalerOption
from lfpreviewer.loading import ImageLoaderOption


class Visibility(enum.Enum):
    VISIBLE = enum.auto()
    INVISIBLE = enum.auto()


class Placement:

    __initialised = False
    __DEFAULT_VALUES = {str: '', int: 0}
    __ATTRIBUTES = {attribute.name: attribute
                    for attribute in attr.fields(_action.AddImageAction)}
    __EMPTY_BASE_PAIRS = (
        lambda attributes, default_values:
        {attribute.name: default_values[attribute.type]
         for attribute in attributes.values()
         if (attribute.default == attr.NOTHING
             and attribute.init)}
        )(__ATTRIBUTES, __DEFAULT_VALUES)

    def __init__(self, canvas, identifier,
                 visibility: Visibility = Visibility.INVISIBLE,
                 **kwargs):

        self.__canvas = canvas
        self.__identifier = identifier
        self.__visibility = False
        self.__data = {}
        self.__initialised = True
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.visibility = visibility

    @property
    def canvas(self):
        return self.__canvas

    @property
    def identifier(self):
        return self.__identifier

    @property
    def visibility(self):
        return self.__visibility

    @visibility.setter
    def visibility(self, value):
        if self.__visibility != value:
            if value is Visibility.INVISIBLE:
                self.__remove()
            elif value is Visibility.VISIBLE:
                self.__update()
            else:
                raise TypeError("expected an instance of Visibility")
            self.__visibility = value

    def __remove(self):
        self.__canvas.enqueue(
            _action.RemoveImageAction(identifier=self.identifier))
        self.__canvas.request_transmission()

    def __update(self):
        self.__canvas.enqueue(_action.AddImageAction(**{
            **self.__data,
            **attr.asdict(_action.Identifiable(identifier=self.identifier))
        }))
        self.__canvas.request_transmission()

    def __getattr__(self, name):
        if name not in self.__ATTRIBUTES:
            raise AttributeError("There is no attribute named %s" % name)

        attribute = self.__ATTRIBUTES[name]

        if name in self.__data:
            return self.__data[name]
        if attribute.default != attr.NOTHING:
            return attribute.default
        return None

    def __setattr__(self, name, value):
        if not self.__initialised:
            super().__setattr__(name, value)
            return
        if name not in self.__ATTRIBUTES:
            if hasattr(self, name):
                super().__setattr__(name, value)
                return
            raise AttributeError("There is no attribute named %s" % name)

        data = dict(self.__data)
        self.__data.update(attr.asdict(_action.AddImageAction(**{
            **self.__EMPTY_BASE_PAIRS,
            **self.__data,
            **attr.asdict(_action.Identifiable(identifier=self.identifier)),
            name: value
        })))

        # remove the key's of the empty base pairs
        # so the developer is forced to set them by himself
        for key in self.__EMPTY_BASE_PAIRS:
            if key not in data and key != name:
                del self.__data[key]

        if self.visibility is Visibility.VISIBLE:
            self.__update()


class UeberzugProcess:
    __KILL_TIMEOUT_SECONDS = 1
    __BUFFER_SIZE_BYTES = 50 * 1024

    def __init__(self, options):
        self.__start_options = options
        self.__process = None

    @property
    def stdin(self):
        return self.__process.stdin

    @property
    def running(self):
        return (self.__process is not None
                and self.__process.poll() is None)

    @property
    def responsive(self):
        return self.running and not self.__process.stdin.closed

    def start(self):
        if self.responsive:
            return
        if self.running:
            self.stop()

        self.__process = subprocess.Popen(
            ['lfpreviewer', 'layer'] + self.__start_options,
            stdin=subprocess.PIPE,
            bufsize=self.__BUFFER_SIZE_BYTES,
            universal_newlines=True,
            start_new_session=True)

    def stop(self):
        if self.running:
            timer_kill = None

            try:
                lfpreviewer_pgid = os.getpgid(self.__process.pid)
                own_pgid = os.getpgid(0)
                assert lfpreviewer_pgid != own_pgid
                timer_kill = threading.Timer(
                    self.__KILL_TIMEOUT_SECONDS,
                    os.killpg,
                    [lfpreviewer_pgid, signal.SIGKILL])

                self.__process.terminate()
                timer_kill.start()
                self.__process.communicate()
            except ProcessLookupError:
                pass
            finally:
                if timer_kill is not None:
                    timer_kill.cancel()


class CommandTransmitter:

    def __init__(self, process):
        self._process = process

    @abc.abstractproperty
    def synchronously_draw(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def enqueue(self, action: _action.Action):
        raise NotImplementedError()

    @abc.abstractmethod
    def transmit(self):
        raise NotImplementedError()


class DequeCommandTransmitter(CommandTransmitter):

    def __init__(self, process):
        super().__init__(process)
        self.__queue_commands = collections.deque()
        self.__synchronously_draw = False

    @property
    def synchronously_draw(self):
        return self.__synchronously_draw

    @synchronously_draw.setter
    def synchronously_draw(self, value):
        self.__synchronously_draw = value

    def enqueue(self, action: _action.Action):
        self.__queue_commands.append(action)

    def transmit(self):
        while self.__queue_commands:
            command = self.__queue_commands.popleft()
            self._process.stdin.write(json.dumps({
                **attr.asdict(command),
                **attr.asdict(_action.Drawable(
                    synchronously_draw=self.__synchronously_draw,
                    draw=not self.__queue_commands))
            }))
            self._process.stdin.write('\n')
        self._process.stdin.flush()


class LazyCommandTransmitter(CommandTransmitter):
    def __init__(self, transmitter):
        super().__init__(None)
        self.transmitter = transmitter

    @property
    def synchronously_draw(self):
        return self.transmitter.synchronously_draw

    @synchronously_draw.setter
    def synchronously_draw(self, value):
        self.transmitter.synchronously_draw = value

    def enqueue(self, action: _action.Action):
        self.transmitter.enqueue(action)

    def transmit(self):
        pass

    def force_transmit(self):
        self.transmitter.transmit()


class Canvas:

    def __init__(self, debug=False):
        self.__process_arguments = (
            ['--loader', ImageLoaderOption.SYNCHRONOUS.value]
            if debug else
            ['--silent'])
        self.__process = None
        self.__transmitter = None
        self.__used_identifiers = set()
        self.automatic_transmission = True

    def create_placement(self, identifier, *args, **kwargs):
        if identifier in self.__used_identifiers:
            raise ValueError("Identifier '%s' is already taken." % identifier)
        self.__used_identifiers.add(identifier)
        return Placement(self, identifier, *args, **kwargs)

    @property
    @contextlib.contextmanager
    def lazy_drawing(self):
        try:
            self.__transmitter.transmit()
            self.__transmitter = LazyCommandTransmitter(self.__transmitter)
            yield
            self.__transmitter.force_transmit()
        finally:
            self.__transmitter = self.__transmitter.transmitter

    @property
    @contextlib.contextmanager
    def synchronous_lazy_drawing(self):
        try:
            self.__transmitter.synchronously_draw = True
            with self.lazy_drawing:
                yield
        finally:
            self.__transmitter.synchronously_draw = False

    def __call__(self, function):
        def decorator(*args, **kwargs):
            with self:
                return function(*args, canvas=self, **kwargs)
        return decorator

    def __enter__(self):
        self.__process = UeberzugProcess(self.__process_arguments)
        self.__transmitter = DequeCommandTransmitter(self.__process)
        self.__process.start()
        return self

    def __exit__(self, *args):
        try:
            self.__process.stop()
        finally:
            self.__process = None
            self.__transmitter = None

    def enqueue(self, command: _action.Action):
        if not self.__process.responsive:
            self.__process.start()

        self.__transmitter.enqueue(command)

    def request_transmission(self, *, force=False):
        if not self.__process.responsive:
            self.__process.start()

        if self.automatic_transmission or force:
            self.__transmitter.transmit()
