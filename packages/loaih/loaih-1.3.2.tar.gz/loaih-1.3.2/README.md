# LibreOffice AppImage Helper - `loaih` #

LibreOffice AppImage Helper is an enhanced Python porting from [previous work
from Antonio
Faccioli](https://github.com/antoniofaccioli/libreoffice-appimage). It helps
building a LibreOffice AppImage from officially released .deb files with some
options.

## Installing the package ##

[![Build Status](https://drone.libreitalia.org/api/badges/libreitalia/loaih/status.svg)](https://drone.libreitalia.org/libreitalia/loaih)

You can much more easily install the package via the produced wheel in the
[Releases](/libreitalia/loaih/releases/) page. Once downloaded, you can
install the utility with `pip`

    $ pip install ./loaih-*.whl

You can also clone the repository and build the app yourself, which is as easy
as:

    $ pip install wheel
    $ git clone https://git.libreitalia.org/libreitalia/loaih.git
    $ cd loaih
    $ python setup.py bdist_wheel
    $ pip install dist/loaih*.whl

## Using the package ##

The package will install a single command, `loaih`, which should help you
build your own version of the AppImage. Here's some usage scenarios.

## Getting options and help ##

You can ask the app some information on how you can use it:

    $ loaih --help
    $ loaih getversion --help
    $ loaih build --help

### Finding metadata on a specific version ###

You can use the command `getversion` and a specific query:

    $ loaih getversion fresh
    $ loaih getversion still

### Building a one-time AppImage ###

You can build yourself an AppImage with specific options:

    $ loaih build -C -a x86_64 -l it -r . -o fresh

This will build an AppImage for the latest "Fresh" version, built for 64-bit
operating systems, with Italian as the only language, with Offline Help,
signed and updatable in the current folder.

For other build options, please see `loaih build --help` which should be
pretty complete.

### Batch building of a set of AppImages ###

This is less documented, but if the *query* parameter to the `build` command
is a YAML file (see references of it in the repository), this will loop
through the various options and create a complete set of builds based on some
characteristics.

    $ loaih build fresh.yml

This is the main way the community builds found at the [LibreOffice AppImage
Repository](https://appimages.libreitalia.org) are produced.
