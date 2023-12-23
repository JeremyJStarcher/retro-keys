use <pcb_outline_with_bit_offset_spec.scad>

linear_extrude(1)
  pcb_traces(layout=layout(), bit=0.2, slices=5, circuits=circuit());
