#!/usr/bin/env python

from dataclasses import dataclass
import fcntl
import os
from pathlib import Path
from enum import Enum
import shutil
from subprocess import Popen
from typing import Dict, Tuple

from threemftool import ThreeMfTool


class SingleInstanceLock:
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.lockfd = None

    def acquire(self):
        self.lockfd = os.open(self.lockfile, os.O_CREAT | os.O_RDWR)
        try:
            fcntl.flock(self.lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    def release(self):
        if self.lockfd:
            os.close(self.lockfd)
            os.unlink(self.lockfile)


class StlMode(Enum):
    KEY_CAP = 1
    LEGEND = 2
    TWO_COLOR = 3


class KeyType(Enum):
    STD = 1
    SPECIAL = 2
    X2 = 3
    CURSOR = 4
    LAYOUT = 5


@dataclass
class KeyInfo:
    key_name: str
    key_type: KeyType
    has_legend: bool


class KeyConverter:
    def __init__(self):
        self.STL_DIR = Path("stls")
        self.VRML_DIR = Path("vrml")
        self.TWO_COLOR_DIR = Path("2-color")
        self.MODEL_TYPE = "3mf"
        self.print_sideways = False
        self.reset()

    def reset(self):
        self.keyType_count: Dict[str, int] = {}

    def getDirectoryForKeyType(self, key_type: KeyType) -> str:
        return {
            KeyType.CURSOR: "cursor",
            KeyType.SPECIAL: "special",
            KeyType.X2: "x2",
            KeyType.STD: "std",
            KeyType.LAYOUT: "layout",
        }.get(key_type, "unknown")

    def getColorForKeyType(self, key_type: KeyType) -> Tuple[str, str]:

        match key_type:
            case KeyType.CURSOR:
                return ("255 255 255 0", "0 0 0 0")
            case KeyType.SPECIAL:
                return ("127 0 0 0", "255 255 255 0")
            case KeyType.X2:
                return ("127 127 127 0", "255 255 255 0")
            case KeyType.STD:
                return ("0 0 0 0", "255 255 255 0")
            case _:
                return ("0 0 255 0", "0 255 0 0")

    def incrementTypeCount(self, key_type: KeyType) -> None:
        key_dir = self.getDirectoryForKeyType(key_type)
        count_key = key_dir
        count = self.keyType_count.get(count_key, 0)
        self.keyType_count.update([(count_key, count + 1)])

    def buildFileName(
        self, dir: Path, keyInfo: KeyInfo, extension: str, mode: StlMode
    ) -> Path:
        tail = ""
        if mode == StlMode.KEY_CAP:
            tail = "cap"
        if mode == StlMode.LEGEND:
            tail = "legend"

        key_dir = self.getDirectoryForKeyType(keyInfo.key_type)
        count_key = key_dir

        count = self.keyType_count.get(count_key, 0)

        subdirIdx = int(count / 10) + 1

        full_key_dir = f"{dir}"

        if extension == self.MODEL_TYPE:
            full_key_dir = f"{dir}/{key_dir}_{subdirIdx}"

        try:
            os.makedirs(full_key_dir)
        except Exception:
            pass

        rr = f"{full_key_dir}/{keyInfo.key_name}_{tail}.{extension}"

        relative = Path(rr)
        absolute = relative.absolute()

        return absolute

    def buildOpenScadCmd(self, keyInfo: KeyInfo, mode: StlMode) -> str:
        tmode = -1
        if mode == StlMode.KEY_CAP:
            tmode = 1
        else:
            tmode = 2

        fileName = self.buildFileName(self.STL_DIR, keyInfo, self.MODEL_TYPE, mode)
        # fileName2 = self.buildFileName(self.STL_DIR, keyInfo, "obj", mode)

        # export_format = 'binstl'
        # export_format = 'asciistl'
        # --export-format {export_format}

        sideways_str = "true" if self.print_sideways else "false"

        cmd = f'flatpak run org.openscad.OpenSCAD -D "key=\\"{keyInfo.key_name}\\"" -D "keymode=\\"{tmode}\\"" -o "{fileName}" -D "print_sideways={sideways_str}" "one_atari_key.scad" '
        return cmd

    # def zip_delete_file(self, src: str, file_to_delete: str) -> None:
    #     def zip_delete_file2(src: str, dest: str, file_to_delete: str) -> None:
    #         """Copy the whole zip file and remove the file we want to delete"""
    #         with ZipFile(src, "r") as zin:
    #             with ZipFile(dest, "w") as zout:
    #                 for item in zin.infolist():
    #                     buffer = zin.read(item.filename)
    #                     if item.filename != file_to_delete:
    #                         zout.writestr(item, buffer)

    #     tmp_file_name = tempfile.gettempprefix() + "tmp_file"
    #     zip_delete_file2(src, tmp_file_name, file_to_delete)
    #     zip_delete_file2(tmp_file_name, src, file_to_delete)
    #     os.remove(tmp_file_name)

    def process_two_color_pair(self, idx: int, keyInfo: KeyInfo) -> None:
        if self.MODEL_TYPE == "3mf":

            threeFm = ThreeMfTool()

            legend_file_name = self.buildFileName(
                self.STL_DIR, keyInfo, self.MODEL_TYPE, StlMode.LEGEND
            )

            keycap_file_name = self.buildFileName(
                self.STL_DIR, keyInfo, self.MODEL_TYPE, StlMode.KEY_CAP
            )

            twocolor_file_name = self.buildFileName(
                self.TWO_COLOR_DIR, keyInfo, self.MODEL_TYPE, StlMode.TWO_COLOR
            )

            threeFm.convert_to_two_color(
                idx,
                legend_file_name,
                keycap_file_name,
                twocolor_file_name,
                Path("empty-cura.3mf"),
                keyInfo.has_legend,
            )

    def key_to_3dmodel(self, keyInfo: KeyInfo) -> None:
        if keyInfo.has_legend:
            cmd1 = self.buildOpenScadCmd(keyInfo, StlMode.KEY_CAP)
            cmd2 = self.buildOpenScadCmd(keyInfo, StlMode.LEGEND)

            process1 = Popen(cmd1, shell=True)
            process2 = Popen(cmd2, shell=True)

            process1.wait()
            process2.wait()
        else:
            cmd1 = self.buildOpenScadCmd(keyInfo, StlMode.KEY_CAP)
            process1 = Popen(cmd1, shell=True)
            process1.wait()

    def make_two_color(self) -> None:
        self._create_dir(self.TWO_COLOR_DIR)

        for idx, keyInfo in enumerate(key_list):
            self.process_two_color_pair(idx, keyInfo)
            self.incrementTypeCount(keyInfo.key_type)

    def make_all_3dmodels(self) -> None:
        self._create_dir(self.STL_DIR)

        for keyInfo in key_list:
            self.key_to_3dmodel(keyInfo)

            self.incrementTypeCount(keyInfo.key_type)

    def make_vrml(self) -> None:
        self._create_dir(self.VRML_DIR)

        for keyInfo in key_list:

            stl1Name = self.buildFileName(
                self.STL_DIR, keyInfo, self.MODEL_TYPE, StlMode.KEY_CAP
            )
            stl2Name = self.buildFileName(
                self.STL_DIR, keyInfo, self.MODEL_TYPE, StlMode.LEGEND
            )

            wrl1Name = self.buildFileName(
                self.VRML_DIR, keyInfo, "wrl", StlMode.KEY_CAP
            )
            wrl2Name = self.buildFileName(self.VRML_DIR, keyInfo, "wrl", StlMode.LEGEND)

            self.incrementTypeCount(keyInfo.key_type)

            exe = "python ../../../py/stl_to_wrl.py"

            colors = self.getColorForKeyType(keyInfo.key_type)
            cap_color = colors[0]
            legend_color = colors[1]

            cmd1 = f"{exe} {stl1Name} {wrl1Name} {cap_color}"
            cmd2 = f"{exe} {stl2Name} {wrl2Name} {legend_color}"

            process1 = Popen(cmd1, shell=True)
            process2 = Popen(cmd2, shell=True)

            process1.wait()
            process2.wait()

    def _create_dir(self, dir_path: Path) -> None:
        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)


key_list = [
    KeyInfo("key_0", KeyType.STD, True),
    KeyInfo("key_1", KeyType.STD, True),
    KeyInfo("key_2", KeyType.STD, True),
    KeyInfo("key_3", KeyType.STD, True),
    KeyInfo("key_4", KeyType.STD, True),
    KeyInfo("key_5", KeyType.STD, True),
    KeyInfo("key_6", KeyType.STD, True),
    KeyInfo("key_7", KeyType.STD, True),
    KeyInfo("key_8", KeyType.STD, True),
    KeyInfo("key_9", KeyType.STD, True),
    KeyInfo("key_a", KeyType.STD, True),
    KeyInfo("key_astrix", KeyType.STD, True),
    KeyInfo("key_b", KeyType.STD, True),
    KeyInfo("key_break", KeyType.X2, True),
    KeyInfo("key_bs", KeyType.SPECIAL, True),
    KeyInfo("key_c", KeyType.STD, True),
    KeyInfo("key_c_down", KeyType.CURSOR, True),
    KeyInfo("key_c_left", KeyType.CURSOR, True),
    KeyInfo("key_c_right", KeyType.CURSOR, True),
    KeyInfo("key_c_up", KeyType.CURSOR, True),
    KeyInfo("key_caps", KeyType.SPECIAL, True),
    KeyInfo("key_comma", KeyType.STD, True),
    KeyInfo("key_control", KeyType.SPECIAL, True),
    KeyInfo("key_d", KeyType.STD, True),
    KeyInfo("key_dash", KeyType.STD, True),
    KeyInfo("key_e", KeyType.STD, True),
    KeyInfo("key_equal", KeyType.STD, True),
    KeyInfo("key_esc", KeyType.SPECIAL, True),
    KeyInfo("key_f", KeyType.STD, True),
    KeyInfo("key_fn", KeyType.SPECIAL, True),
    KeyInfo("key_g", KeyType.STD, True),
    KeyInfo("key_gt", KeyType.STD, True),
    KeyInfo("key_h", KeyType.STD, True),
    KeyInfo("key_help", KeyType.X2, True),
    KeyInfo("key_i", KeyType.STD, True),
    KeyInfo("key_inv", KeyType.X2, True),
    KeyInfo("key_j", KeyType.STD, True),
    KeyInfo("key_k", KeyType.STD, True),
    KeyInfo("key_l", KeyType.STD, True),
    KeyInfo("key_lshift", KeyType.SPECIAL, True),
    KeyInfo("key_lt", KeyType.STD, True),
    KeyInfo("key_m", KeyType.STD, True),
    KeyInfo("key_menu", KeyType.X2, True),
    KeyInfo("key_n", KeyType.STD, True),
    KeyInfo("key_o", KeyType.STD, True),
    KeyInfo("key_option", KeyType.X2, True),
    KeyInfo("key_p", KeyType.STD, True),
    KeyInfo("key_period", KeyType.STD, True),
    KeyInfo("key_plus", KeyType.STD, True),
    KeyInfo("key_power", KeyType.X2, True),
    KeyInfo("key_q", KeyType.STD, True),
    KeyInfo("key_r", KeyType.STD, True),
    KeyInfo("key_reset", KeyType.X2, True),
    KeyInfo("key_return", KeyType.SPECIAL, True),
    KeyInfo("key_rshift", KeyType.SPECIAL, True),
    KeyInfo("key_s", KeyType.STD, True),
    KeyInfo("key_select", KeyType.X2, True),
    KeyInfo("key_semi", KeyType.STD, True),
    KeyInfo("key_slash", KeyType.STD, True),
    KeyInfo("key_space", KeyType.STD, False),
    KeyInfo("key_start", KeyType.X2, True),
    KeyInfo("key_t", KeyType.STD, True),
    KeyInfo("key_tab", KeyType.SPECIAL, True),
    KeyInfo("key_turbo", KeyType.X2, True),
    KeyInfo("key_u", KeyType.STD, True),
    KeyInfo("key_v", KeyType.STD, True),
    KeyInfo("key_w", KeyType.STD, True),
    KeyInfo("key_x", KeyType.STD, True),
    KeyInfo("key_y", KeyType.STD, True),
    KeyInfo("key_z", KeyType.STD, True),
    # KeyInfo("layout", KeyType.LAYOUT, True),
]

if __name__ == "__main__":
    lock = SingleInstanceLock("/tmp/myscript.lock")
    if not lock.acquire():
        print("Another instance of this script is already running. Exiting.")
        exit(1)

    converter = KeyConverter()
    converter.MODEL_TYPE = "3mf"
    converter.STL_DIR = Path("3mfs")
    converter.print_sideways = True
    # converter.make_all_3dmodels()
    converter.reset()
    converter.make_two_color()

    # converter = KeyConverter()
    # converter.MODEL_TYPE = "stl"
    # converter.STL_DIR = Path("stls")
    # converter.print_sideways = False
    # converter.make_all_3dmodels()
    # converter.reset()
    # converter.make_vrml()

    lock.release()
