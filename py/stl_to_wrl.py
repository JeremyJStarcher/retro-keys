# type: ignore
import pymeshlab
import sys


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
    else:
        src = sys.argv[1]
        dest = sys.argv[2]
        r = sys.argv[3]
        g = sys.argv[4]
        b = sys.argv[5]
        a = sys.argv[6]

        color = pymeshlab.Color(int(r), int(g), int(b), int(a))
        print("Converting.." + src)
        stl_to_wrl(src, dest, color)
