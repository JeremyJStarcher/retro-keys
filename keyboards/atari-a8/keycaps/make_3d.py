#!/usr/bin/env python

from dataclasses import dataclass
import fcntl
import os
from pathlib import Path
from enum import Enum
import shutil
from subprocess import Popen
from typing import Dict, Optional, Tuple
import time

# type: ignore
import trimesh
from threemftool import ThreeMfTool

THREE_D_ROOT = "keycap-models"


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


class SlicerTarget(Enum):
    CURA = 1
    BAMBU = 2


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
        self.SRC_DIR: Optional[Path] = None
        self.DEST_DIR: Optional[Path] = None
        self.pocket_src = False
        self.pocket_dest = False

        self.openscad_model_output: str = ""
        self.openscad_model_sideways = False
        self.reset()

    def reset(self):
        self.SRC_DIR = None
        self.DEST_DIR = None
        self.pocket_src = False
        self.pocket_dest = False

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
                return ("255 255 255 255", "0 0 0 0")
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
        self,
        dir: Optional[Path],
        pocket: bool,
        keyInfo: KeyInfo,
        extension: str,
        keycap_mode: StlMode,
    ) -> Path:
        tail = ""
        if keycap_mode == StlMode.KEY_CAP:
            tail = "cap"
        if keycap_mode == StlMode.LEGEND:
            tail = "legend"

        if dir is None:
            raise Exception("ACK")

        key_dir = self.getDirectoryForKeyType(keyInfo.key_type)
        count_key = key_dir

        count = self.keyType_count.get(count_key, 0)

        subdirIdx = int(count / 10) + 1

        full_key_dir = f"{dir}"

        if pocket:
            full_key_dir = f"{dir}/{key_dir}_{subdirIdx}"

        Path(full_key_dir).mkdir(parents=True, exist_ok=True)

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

        fileName = self.buildFileName(
            self.DEST_DIR, self.pocket_dest, keyInfo, self.openscad_model_output, mode
        )

        sideways_str = "true" if self.openscad_model_sideways else "false"

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

    def process_two_color_pair(
        self, idx: int, keyInfo: KeyInfo, slicerTarget: SlicerTarget
    ) -> None:
        if self.openscad_model_output == "3mf":

            threeFm = ThreeMfTool()

            legend_file_name = self.buildFileName(
                self.SRC_DIR,
                self.pocket_src,
                keyInfo,
                self.openscad_model_output,
                StlMode.LEGEND,
            )

            keycap_file_name = self.buildFileName(
                self.SRC_DIR,
                self.pocket_src,
                keyInfo,
                self.openscad_model_output,
                StlMode.KEY_CAP,
            )

            twocolor_file_name = self.buildFileName(
                self.DEST_DIR,
                self.pocket_src,
                keyInfo,
                self.openscad_model_output,
                StlMode.TWO_COLOR,
            )

            if slicerTarget == SlicerTarget.CURA:
                threeFm.cura_convert_to_two_color(
                    idx,
                    legend_file_name,
                    keycap_file_name,
                    twocolor_file_name,
                    Path("empty-cura.3mf"),
                    keyInfo.has_legend,
                )

    def openscad_to_model(self, keyInfo: KeyInfo) -> None:
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

    def make_two_color(self, slicerTarget: SlicerTarget) -> None:
        self._create_dir(self.DEST_DIR)

        for idx, keyInfo in enumerate(key_list):
            self.process_two_color_pair(idx, keyInfo, slicerTarget)
            self.incrementTypeCount(keyInfo.key_type)

    def make_openscad_models(self) -> None:
        self._create_dir(self.DEST_DIR)

        for keyInfo in key_list:
            self.openscad_to_model(keyInfo)

            self.incrementTypeCount(keyInfo.key_type)

    def convert_3mfs_to_stls(self):
        self._create_dir(self.DEST_DIR)

        def copy_one(keyInfo: KeyInfo, stl_mode: StlMode):
            file_name_3mf = self.buildFileName(
                self.SRC_DIR, self.pocket_src, keyInfo, "3mf", stl_mode
            )
            file_name_stl = self.buildFileName(
                self.DEST_DIR, self.pocket_dest, keyInfo, "stl", stl_mode
            )

            mesh = trimesh.load(file_name_3mf)
            mesh.export(file_name_stl)

        for keyInfo in key_list:
            copy_one(keyInfo, StlMode.KEY_CAP)

            if keyInfo.has_legend:
                copy_one(keyInfo, StlMode.LEGEND)

            self.incrementTypeCount(keyInfo.key_type)

    def make_vrml(self) -> None:
        self._create_dir(self.DEST_DIR)

        for keyInfo in key_list:
            stl1Name = self.buildFileName(
                self.SRC_DIR, self.pocket_src, keyInfo, "stl", StlMode.KEY_CAP
            )
            stl2Name = self.buildFileName(
                self.SRC_DIR, self.pocket_src, keyInfo, "stl", StlMode.LEGEND
            )

            wrl1Name = self.buildFileName(
                self.DEST_DIR, self.pocket_dest, keyInfo, "wrl", StlMode.KEY_CAP
            )
            wrl2Name = self.buildFileName(
                self.DEST_DIR, self.pocket_dest, keyInfo, "wrl", StlMode.LEGEND
            )

            self.incrementTypeCount(keyInfo.key_type)

            exe = "python ../../../py/stl_to_wrl.py"

            colors = self.getColorForKeyType(keyInfo.key_type)
            cap_color = colors[0]
            legend_color = colors[1]

            cmd1 = f"{exe} {stl1Name} {wrl1Name} {cap_color}"
            cmd2 = f"{exe} {stl2Name} {wrl2Name} {legend_color}"

            if keyInfo.has_legend:
                process1 = Popen(cmd1, shell=True)
                process2 = Popen(cmd2, shell=True)

                process1.wait()
                process2.wait()
            else:
                process1 = Popen(cmd1, shell=True)
                process1.wait()

    def _create_dir(self, dir_path: Optional[Path]) -> None:
        if dir_path is None:
            raise Exception("_create_dir: dir not set")

        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)


key_list = [
    KeyInfo("key_0", KeyType.STD, True),
    KeyInfo("key_1", KeyType.STD, True),
    # KeyInfo("key_2", KeyType.STD, True),
    # KeyInfo("key_3", KeyType.STD, True),
    # KeyInfo("key_4", KeyType.STD, True),
    # KeyInfo("key_5", KeyType.STD, True),
    # KeyInfo("key_6", KeyType.STD, True),
    # KeyInfo("key_7", KeyType.STD, True),
    # KeyInfo("key_8", KeyType.STD, True),
    # KeyInfo("key_9", KeyType.STD, True),
    # KeyInfo("key_a", KeyType.STD, True),
    # KeyInfo("key_astrix", KeyType.STD, True),
    # KeyInfo("key_b", KeyType.STD, True),
    # KeyInfo("key_break", KeyType.X2, True),
    # KeyInfo("key_bs", KeyType.SPECIAL, True),
    # KeyInfo("key_c", KeyType.STD, True),
    # KeyInfo("key_c_down", KeyType.CURSOR, True),
    # KeyInfo("key_c_left", KeyType.CURSOR, True),
    # KeyInfo("key_c_right", KeyType.CURSOR, True),
    # KeyInfo("key_c_up", KeyType.CURSOR, True),
    # KeyInfo("key_caps", KeyType.SPECIAL, True),
    # KeyInfo("key_comma", KeyType.STD, True),
    # KeyInfo("key_control", KeyType.SPECIAL, True),
    # KeyInfo("key_d", KeyType.STD, True),
    # KeyInfo("key_dash", KeyType.STD, True),
    # KeyInfo("key_e", KeyType.STD, True),
    # KeyInfo("key_equal", KeyType.STD, True),
    # KeyInfo("key_esc", KeyType.SPECIAL, True),
    # KeyInfo("key_f", KeyType.STD, True),
    # KeyInfo("key_fn", KeyType.SPECIAL, True),
    # KeyInfo("key_g", KeyType.STD, True),
    # KeyInfo("key_gt", KeyType.STD, True),
    # KeyInfo("key_h", KeyType.STD, True),
    # KeyInfo("key_help", KeyType.X2, True),
    # KeyInfo("key_i", KeyType.STD, True),
    # KeyInfo("key_inv", KeyType.X2, True),
    # KeyInfo("key_j", KeyType.STD, True),
    # KeyInfo("key_k", KeyType.STD, True),
    # KeyInfo("key_l", KeyType.STD, True),
    # KeyInfo("key_lshift", KeyType.SPECIAL, True),
    # KeyInfo("key_lt", KeyType.STD, True),
    # KeyInfo("key_m", KeyType.STD, True),
    # KeyInfo("key_menu", KeyType.X2, True),
    # KeyInfo("key_n", KeyType.STD, True),
    # KeyInfo("key_o", KeyType.STD, True),
    # KeyInfo("key_option", KeyType.X2, True),
    # KeyInfo("key_p", KeyType.STD, True),
    # KeyInfo("key_period", KeyType.STD, True),
    # KeyInfo("key_plus", KeyType.STD, True),
    # KeyInfo("key_power", KeyType.X2, True),
    # KeyInfo("key_q", KeyType.STD, True),
    # KeyInfo("key_r", KeyType.STD, True),
    # KeyInfo("key_reset", KeyType.X2, True),
    # KeyInfo("key_return", KeyType.SPECIAL, True),
    # KeyInfo("key_rshift", KeyType.SPECIAL, True),
    # KeyInfo("key_s", KeyType.STD, True),
    # KeyInfo("key_select", KeyType.X2, True),
    # KeyInfo("key_semi", KeyType.STD, True),
    # KeyInfo("key_slash", KeyType.STD, True),
    # KeyInfo("key_space", KeyType.STD, False),
    # KeyInfo("key_start", KeyType.X2, True),
    # KeyInfo("key_t", KeyType.STD, True),
    # KeyInfo("key_tab", KeyType.SPECIAL, True),
    # KeyInfo("key_turbo", KeyType.X2, True),
    # KeyInfo("key_u", KeyType.STD, True),
    # KeyInfo("key_v", KeyType.STD, True),
    # KeyInfo("key_w", KeyType.STD, True),
    # KeyInfo("key_x", KeyType.STD, True),
    # KeyInfo("key_y", KeyType.STD, True),
    # KeyInfo("key_z", KeyType.STD, True),
    # # KeyInfo("layout", KeyType.LAYOUT, True),
]


def run_main():

    lock = SingleInstanceLock("/tmp/myscript.lock")
    if not lock.acquire():
        print("Another instance of this script is already running. Exiting.")
        exit(1)

    converter = KeyConverter()

    SIDEWAYS_3MF_PATH = Path(f"{THREE_D_ROOT}/3mfs-openscad")
    CURA_SIDEWAYS_2COLOR_3MF_PATH = Path(f"{THREE_D_ROOT}/two-color-cura")
    BAMBU_SIDEWAYS_2COLOR_3MF_PATH = Path(f"{THREE_D_ROOT}/two-color-bambu")

    FLAT_3MF_PATH = Path(f"{THREE_D_ROOT}/3mfs-flat-openscad")
    FLAT_2COLOR_3MF_PATH = Path(f"{THREE_D_ROOT}/two-color-flat")
    FLAT_STL_PATH = Path(f"{THREE_D_ROOT}/flat-stl")
    VMRL_PATH = Path(f"{THREE_D_ROOT}/vrml")

    converter.reset()
    converter.openscad_model_output = "3mf"
    converter.openscad_model_sideways = True
    converter.DEST_DIR = SIDEWAYS_3MF_PATH
    converter.pocket_dest = True
    converter.make_openscad_models()

    converter.reset()
    converter.DEST_DIR = CURA_SIDEWAYS_2COLOR_3MF_PATH
    converter.pocket_dest = True
    converter.SRC_DIR = SIDEWAYS_3MF_PATH
    converter.pocket_src = True
    converter.make_two_color(SlicerTarget.CURA)

    converter.reset()
    converter.openscad_model_output = "3mf"
    converter.openscad_model_sideways = False
    converter.DEST_DIR = FLAT_3MF_PATH
    converter.pocket_dest = True
    converter.make_openscad_models()

    converter.reset()
    converter.SRC_DIR = FLAT_3MF_PATH
    converter.pocket_src = True
    converter.DEST_DIR = FLAT_STL_PATH
    converter.pocket_dest = False
    converter.convert_3mfs_to_stls()

    converter.reset()
    converter.SRC_DIR = FLAT_STL_PATH
    converter.pocket_src = False
    converter.DEST_DIR = VMRL_PATH
    converter.pocket_dest = False
    converter.make_vrml()

    lock.release()


if __name__ == "__main__":
    start_time = time.time()
    run_main()
    end_time = time.time()

    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, _ = divmod(remainder, 60)

    print(f"Runtime: {int(hours)} hours, {int(minutes)} minutes")
