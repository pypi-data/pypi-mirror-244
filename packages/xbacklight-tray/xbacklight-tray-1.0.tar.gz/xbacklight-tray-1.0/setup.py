from setuptools import setup, find_packages

def get_long_description():
    with open('README.md') as f:
        return f.read()

setup(
    name='xbacklight-tray',
    version='1.0',
    license='GPLv3',
    author="Vasily Mikhaylichenko",
    author_email='vasily@lxmx.org',
    url='https://github.com/lxmx/xbacklight-tray',
    install_requires=[
          'PyGObject',
    ],
    scripts=["xbacklight-tray"],
    packages=find_packages('.'),
    description='GTK tray icon to adjust backlight brightness',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        "Operating System :: PDA Systems",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment",
        "Topic :: System :: Hardware",
        "Topic :: Utilities",
        "Topic :: Desktop Environment :: Window Managers",
    ],
)
