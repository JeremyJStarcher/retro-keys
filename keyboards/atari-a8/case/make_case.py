#!/usr/bin/env python

from subprocess import Popen
import os
from pathlib import Path

STL_DIR="stls"

def makeCommand(pieces: int, piece: int):
    fileName = Path(STL_DIR,  f"CASE_{pieces}_{piece}.stl")
    cmd = f'flatpak run org.openscad.OpenSCAD -D "CASE_PIECES={pieces}" -D "CASE_PIECE={piece}" -o "{fileName}" "case-position.scad" --export-format binstl'
    return cmd

def make4():
    cmd1 = makeCommand(4, 1)
    cmd2 = makeCommand(4, 2)
    cmd3 = makeCommand(4, 3)
    cmd4 = makeCommand(4, 4)

    process1 = Popen(cmd1, shell=True)
    process2 = Popen(cmd2, shell=True)
    process3 = Popen(cmd3, shell=True)
    process4 = Popen(cmd4, shell=True)

    process1.wait()
    process2.wait()
    process3.wait()
    process4.wait()


os.makedirs(STL_DIR)
make4();