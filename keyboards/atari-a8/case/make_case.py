#!/usr/bin/env python

from subprocess import Popen
import os
from pathlib import Path
import shutil

STL_DIR = "stls"


def makeCommand(pieces: int, piece: int):
    fileName = Path(STL_DIR, f"CASE_{pieces}_{piece}.stl")
    cmd = f'flatpak run org.openscad.OpenSCAD -D "CASE_PIECES={pieces}" -D "CASE_PIECE={piece}" -o "{fileName}" "case-position.scad" --export-format binstl'
    return cmd


def make():
    cmd_4_1 = makeCommand(4, 1)
    cmd_4_2 = makeCommand(4, 2)
    cmd_4_3 = makeCommand(4, 3)
    cmd_4_4 = makeCommand(4, 4)

    cmd_2_1 = makeCommand(2, 1)
    cmd_2_2 = makeCommand(2, 2)

    process_4_1 = Popen(cmd_4_1, shell=True)
    process_4_2 = Popen(cmd_4_2, shell=True)
    process_4_3 = Popen(cmd_4_3, shell=True)
    process_4_4 = Popen(cmd_4_4, shell=True)

    process_2_1 = Popen(cmd_2_1, shell=True)
    process_2_2 = Popen(cmd_2_2, shell=True)

    process_4_1.wait()
    process_4_2.wait()
    process_4_3.wait()
    process_4_4.wait()

    process_2_1.wait()
    process_2_2.wait()


try:
    shutil.rmtree(STL_DIR, ignore_errors=False, onerror=None)
except Exception:
    pass

os.makedirs(STL_DIR)
make()
