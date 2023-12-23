use <pcb_outline_with_bit_offset_spec.scad>

linear_extrude(1)
  pcb_traces(layout=layout(), circuits=circuit());
