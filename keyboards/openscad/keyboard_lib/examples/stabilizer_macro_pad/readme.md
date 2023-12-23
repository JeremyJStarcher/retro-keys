# Stabilizer Tester Macropad

This is a macropad design that is mostly used for testing stabilizers.

Each piece that needs generation is in a separate file so it can be generated
programmatically. The layout is kept in `layout.scad` and then imported into each
object's individual files.

## Generate the Files
```
openscad -o tmp/pcb_drill.dxf examples/stabilizer_macro_pad/pcb_drill.scad
openscad -o tmp/pcb_traces.dxf examples/stabilizer_macro_pad/pcb_traces.scad
openscad -o tmp/pcb_outline.dxf examples/stabilizer_macro_pad/pcb_outline.scad
openscad -o tmp/plate.dxf examples/stabilizer_macro_pad/plate.scad
openscad -o tmp/bottom_case.stl examples/stabilizer_macro_pad/bottom_case.scad
openscad -o tmp/top_case.stl examples/stabilizer_macro_pad/top_case.scad
```
