# retro-keys

Retro Keyboards for Emulators

## Purpose

The purpose of this project is to set up a tools to make it easier to create
a custom keyboard to use retro-style computers on modern emulators.

This includes the PCB, keycaps and (in time) a case.

Better integration with [QMK](https://qmk.fm/) is planned.

## Keyboard support

* Atari 800/800XL style keyboard.

## Requirements

* Python 3.10
* OpenSCAD
* KiCad
* VcCode (other editors will work but may require configuration)

## After clone

All of the Python scripts run in a `virtual environment` which will allow them to
access privately installed libraries.

### Step 1 - Install Python `venv`

This package must be installed globally.

    pip install venv

### Step 2 - Create the virtual environment (only needs done once after clone)

In your shell/commandline of choice, change directory to the project root `py`
directory.

    python3 -m venv .venv

### Step 3 - Enter virtual environment (needs done every time you with with `retro-keys`)

From the `py` directory, enter the following command

Linux/Unix:

    source .venv/bin/activate

### Step 4 - Install the required libraries into the virtual environment.

    ./py_libs.sh

## Directory layout

The `keyboards` directory contains the data required for each unique keyboard
as well as common code (and graphics) libraries that are used by all keyboards.

    * `atari-a8` - Keyboard 800/800XL layout
    * `c64-vic20` - C64/VIC20 keyboard (in development)
    * `kicad-lib` - Graphics libraries
    * `openscad` - Open SCAD libraries
    * `retrologo-kb` - Fake keyboard used to generate website graphics.

For each actual keyboard, the directory structure is:

    * `kicad` - The KiCad project for that keyboard
    * `keycaps` - The OpenSCAD scripts to generate the keyboard.

It is important to note that the generated key graphics, stl and wrl files are NOT
checked into the repo as they would take up a large amount of space and must be
regenerated when working on that keyboard.

### Working with an existing keyboard

Yet to be documented.  This workflow is still somewhat reliant on a QMK script
outside the `retro-keys` project directory structure.
