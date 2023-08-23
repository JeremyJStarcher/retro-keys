# type: ignore
import pymeshlab
import sys


"""
This code is in the regular `py` directory so that it can access any installed
libraries of the environment.

Trying to load this as a module for something entirely outside of this directory
structure proved to be problematic so it can be run as a stand alone program.
"""


def stl_to_wrl(src: str, dest: str, color: pymeshlab.Color):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(src)

    # m = ms.current_mesh()
    # v_matrix = m.vertex_matrix()
    # print(v_matrix)

    #    ms.set_color_per_vertex(color1=pymeshlab.Color(255, 0, 0, 0))  # [0, 0, 0, 255], False)
    ms.set_color_per_vertex(color1=color)
    ms.save_current_mesh(dest)


if __name__ == "__main__":
    #    print ('Number of arguments:', len(sys.argv), 'arguments.')
    #    print ('Argument List:', str(sys.argv))

    if len(sys.argv) < 7:
        print("stl_to_wrl is not to be called directly.")
        print("This is used by the keycap generators to convert")
        print("stl files to wrl to use as KiCad 3d models")

        print("")
        print(f"python {sys.argv[0]} src dest red green blue alpha")
        print("")
        print("Absolute path names for `src` and `dest` recommend")
    else:
        src = sys.argv[1]
        dest = sys.argv[2]
        r = sys.argv[3]
        g = sys.argv[4]
        b = sys.argv[5]
        a = sys.argv[6]

        color = pymeshlab.Color(int(r), int(g), int(b), int(a))
        # print("Converting.." + src)
        stl_to_wrl(src, dest, color)
