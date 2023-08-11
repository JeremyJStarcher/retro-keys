#!/usr/bin/env python

import shutil
import os
from subprocess import Popen
from enum import Enum
from pathlib import Path

class StlMode(Enum):
    KEY_CAP = 1
    INSET = 2


STL_DIR="stls"
VRML_DIR="vrml"


def buildFileName(dir, key_name, extension, mode):
   tmode = -1
   if mode == StlMode.KEY_CAP:
      tail = "cap"
      tmode = 1
   else:
      tail = "legend"
      tmode = 2


   rr =f"{dir}/{key_name}_{tail}.{extension}" 

   relative = Path(rr)
   absolute = relative.absolute()

   return absolute 

def buildOpenScadCmd(key_name, mode):
   tmode = -1
   if mode == StlMode.KEY_CAP:
      tmode = 1
   else:
      tmode = 2

   fileName = buildFileName(STL_DIR, key_name, "stl", mode)
   cmd = f'flatpak run org.openscad.OpenSCAD -D "key=\\"{key_name}\\"" -D "keymode=\\"{tmode}\\"" -o "{fileName}" "one_atari_key.scad" --export-format binstl'
   return cmd

def key_to_stl(key_name):
   cmd1 = buildOpenScadCmd(key_name, StlMode.KEY_CAP)
   cmd2 = buildOpenScadCmd(key_name, StlMode.INSET)

   print(key_name)
   print(cmd1)

   process1 = Popen(cmd1, shell=True)
   process2 = Popen(cmd2, shell=True)

   process1.wait()
   process2.wait()


def make_all_stls():

   try:
      shutil.rmtree(STL_DIR, ignore_errors=False, onerror=None)
   except Exception:
      pass

   os.makedirs(STL_DIR)

   for key in key_list:
      key_to_stl(key)

def make_vrml():

   try:
      shutil.rmtree(VRML_DIR, ignore_errors=False, onerror=None)
   except Exception:
      pass

   os.makedirs(VRML_DIR)

   for key in key_list:
      stl1Name = buildFileName(STL_DIR, key, "stl", StlMode.KEY_CAP)
      stl2Name = buildFileName(STL_DIR, key, "stl", StlMode.INSET)

      wrl1Name = buildFileName(VRML_DIR, key, "wrl", StlMode.KEY_CAP)
      wrl2Name = buildFileName(VRML_DIR, key, "wrl", StlMode.INSET)

      exe = "python ../../../py/stl_to_wrl.py"

      cmd1 = f'{exe} {stl1Name} {wrl1Name} 0 0 0 0'
      cmd2 = f'{exe} {stl2Name} {wrl2Name} 255 255 255 0'

      process1 = Popen(cmd1, shell=True)
      process2 = Popen(cmd2, shell=True)

      process1.wait()
      process2.wait()

key_list = [
   "key_0",
   "key_1",
   "key_2",
   "key_3",
   "key_4",
   "key_5",
   "key_6",
   "key_7",
   "key_8",
   "key_9",
   "key_a",
   "key_astrix",
   "key_b",
   "key_break",
   "key_bs",
   "key_c",
   "key_c_down",
   "key_c_left",
   "key_c_right",
   "key_c_up",
   "key_caps",
   "key_comma",
   "key_control",
   "key_d",
   "key_dash",
   "key_e",
   "key_equal",
   "key_esc",
   "key_f",
   "key_fn",
   "key_g",
   "key_gt",
   "key_h",
   "key_help",
   "key_i",
   "key_inv",
   "key_j",
   "key_k",
   "key_l",
   "key_lshift",
   "key_lt",
   "key_m",
   "key_menu",
   "key_n",
   "key_o",
   "key_option",
   "key_p",
   "key_period",
   "key_plus",
   "key_power",
   "key_q",
   "key_r",
   "key_reset",
   "key_return",
   "key_rshift",
   "key_s",
   "key_select",
   "key_semi",
   "key_slash",
   "key_space",
   "key_start",
   "key_t",
   "key_tab",
   "key_turbo",
   "key_u",
   "key_v",
   "key_w",
   "key_x",
   "key_y",
   "key_z"
   #"layout"
]

if __name__ == '__main__':
   make_all_stls()
   make_vrml()
