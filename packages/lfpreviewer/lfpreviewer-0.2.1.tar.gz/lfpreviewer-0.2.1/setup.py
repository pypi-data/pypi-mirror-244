#!/usr/bin/env python3

import setuptools
import glob

setuptools.setup(
    name='lfpreviewer',
    version='0.2.1',
    description='Previewer for lfp',
    license='GPLv3',
    python_requires='>=3.6',
    install_requires=['docopt', 'attrs>=18.2.0', 'pillow'],
    include_package_data=True,
    package_data={ '': ['*.sh'] },
    packages=setuptools.find_packages(),
    entry_points={ 'console_scripts': [
        'lfpreviewer=lfpreviewer.__main__:main'
    ]},
    ext_modules=[
        setuptools.Extension("lfpreviewer.X", glob.glob("lfpreviewer/X/*.c"),
        libraries=["X11", "Xext", "XRes"], include_dirs=["lfpreviewer/X"]),
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Operating System :: POSIX :: Linux'
    ]
)
