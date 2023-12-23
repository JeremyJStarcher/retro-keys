include <utilities.scad>
include <variables.scad>
include <circuits/ec11.scad>
include <circuits/mts_101.scad>
include <circuits/pro_micro.scad>
include <circuits/proton_c.scad>
include <circuits/support.scad>
include <circuits/trace.scad>
include <circuits/trrs.scad>
include <circuits/wire.scad>

function circuit_position(loc) = [
  len(loc) < 1 ? 0 : u_mm(loc[0]),
  len(loc) < 2 ? 0 : u_mm(loc[1]),
  len(loc) < 3 ? 0 : loc[2],
  len(loc) < 4 ? 0 : loc[3],
  len(loc) < 5 ? "pro_micro" : loc[4],
  len(loc) < 6 ? undef : loc[5]
];

module circuits_pcb_drill(locations) {
  if(len(locations) > 0) {
    circuits_pcb_drill(pop(locations));
    location = circuit_position(locations[0]);
    translate([location[0],location[1],location[2]]) 
      rotate(location[3]) {
        if(location[4] == "pro_micro") {
          pro_micro_pcb_drill(location[5] == undef ? "holes" : location[4]);
        }
        if(location[4] == "trrs_left") {
          trrs_pcb_drill(side="left");
        }
        if(location[4] == "trrs_right") {
          trrs_pcb_drill(side="right");
        }
        if(location[4] == "trrs") {
          trrs_pcb_drill(side="none");
        }
        if(location[4] == "proton_c") {
          proton_c_pcb_drill(size="full");
        }
        if(location[4] == "proton_c_short") {
          proton_c_pcb_drill(size="short");
        }
        if(location[4] == "ec11") {
          ec11_pcb_drill(connections=location[5], single=true);
        }
        if(location[4] == "ec11_double") {
          ec11_pcb_drill(connections=location[5], single=false);
        }
        if(location[4] == "mts_101") {
          mts_101_pcb_drill();
        }
        if(location[4] == "wire_12") {
          wire_pcb_drill(12);
        }
        if(location[4] == "wire_14") {
          wire_pcb_drill(14);
        }
        if(location[4] == "wire_10") {
          wire_pcb_drill(10);
        }
        if(location[4] == "wire_8") {
          wire_pcb_drill(8);
        }
        if(location[4] == "wire_16") {
          wire_pcb_drill(16);
        }
        if(location[4] == "support_2mm") {
          wire_pcb_drill(2);
        }
        if(location[4] == "supprt_3mm") {
          wire_pcb_drill(3);
        }
        if(location[4] == "support_4mm") {
          wire_pcb_drill(4);
        }
        if(location[4] == "manual_trace") {
          assert(len(location[5]) > 0, "Manual trace must provide vector.");
          manual_trace_pcb_drill(locations[0]);
        }
      }
  }
}

module circuits_pcb_traces(locations) {
  if(len(locations) > 0) {
    circuits_pcb_traces(pop(locations));
    location = circuit_position(locations[0]);
    translate([location[0],location[1],location[2]])
      rotate(location[3]) {
        if(location[4] == "pro_micro") {
          pro_micro_pcb_traces(location[5] == undef ? "holes" : location[4]);
        }
        if(location[4] == "trrs_left") {
          trrs_pcb_traces(side="left");
        }
        if(location[4] == "trrs_right") {
          trrs_pcb_traces(side="right");
        }
        if(location[4] == "trrs") {
          trrs_pcb_traces(side="none");
        }
        if(location[4] == "proton_c") {
          proton_c_pcb_traces(size="full");
        }
        if(location[4] == "proton_c_short") {
          proton_c_pcb_traces(size="short");
        }
        if(location[4] == "ec11") {
          ec11_pcb_traces(connections=location[5], single=true);
        }
        if(location[4] == "ec11_double") {
          ec11_pcb_traces(connections=location[5], single=false);
        }
        if(location[4] == "mts_101") {
          mts_101_pcb_traces();
        }
        if(location[4] == "wire_12") {
          wire_pcb_traces(12);
        }
        if(location[4] == "wire_14") {
          wire_pcb_traces(14);
        }
        if(location[4] == "wire_10") {
          wire_pcb_traces(10);
        }
        if(location[4] == "wire_8") {
          wire_pcb_traces(8);
        }
        if(location[4] == "wire_16") {
          wire_pcb_traces(16);
        }
        if(location[4] == "support_2mm") {
          support_pcb_traces(2);
        }
        if(location[4] == "suppot_3mm") {
          support_pcb_traces(3);
        }
        if(location[4] == "support_4mm") {
          support_pcb_traces(4);
        }
        if(location[4] == "manual_trace") {
          assert(len(location[5]) > 0, "Manual trace must provide vector.");
          manual_trace_pcb_traces(locations[0]);
        }
      }
  }
}

module circuits_pcb_traces_bottom(locations) {
  if(len(locations) > 0) {
    circuits_pcb_traces_bottom(pop(locations));
    location = circuit_position(locations[0]);
    translate([location[0],location[1],location[2]])
      rotate(location[3]) {
        if(location[4] == "pro_micro") {
          pro_micro_pcb_traces(location[5] == undef ? "holes" : location[4]);
        }
        if(location[4] == "trrs_left") {
          trrs_pcb_traces(side="left");
        }
        if(location[4] == "trrs_right") {
          trrs_pcb_traces(side="right");
        }
        if(location[4] == "trrs") {
          trrs_pcb_traces(side="none");
        }
        if(location[4] == "proton_c") {
          proton_c_pcb_traces(size="full");
        }
        if(location[4] == "proton_c_short") {
          proton_c_pcb_traces(size="short");
        }
        if(location[4] == "ec11") {
          ec11_pcb_traces(connections=location[5], single=true);
        }
        if(location[4] == "ec11_double") {
          ec11_pcb_traces_bottom(connections=location[5]);
        }
        if(location[4] == "mts_101") {
          mts_101_pcb_traces();
        }
        if(location[4] == "wire_12") {
          wire_pcb_traces(12);
        }
        if(location[4] == "wire_14") {
          wire_pcb_traces(14);
        }
        if(location[4] == "wire_10") {
          wire_pcb_traces(10);
        }
        if(location[4] == "wire_8") {
          wire_pcb_traces(8);
        }
        if(location[4] == "wire_16") {
          wire_pcb_traces(16);
        }
        if(location[4] == "support_2mm") {
          support_pcb_traces(2);
        }
        if(location[4] == "suppot_3mm") {
          support_pcb_traces(3);
        }
        if(location[4] == "support_4mm") {
          support_pcb_traces(4);
        }
        if(location[4] == "manual_trace") {
          assert(len(location[5]) > 0, "Manual trace must provide vector.");
          manual_trace_pcb_traces_bottom(locations[0]);
        }
      }
  }
}

module circuits_pcb_outline(locations) {
  if(len(locations) > 0) {
    circuits_pcb_outline(pop(locations));
    location = circuit_position(locations[0]);
    translate([location[0],location[1],location[2]]) 
      rotate(location[3]) {
        if(location[4] == "pro_micro") {
          pro_micro_pcb_outline();
        }
        if(location[4] == "trrs_left") {
          trrs_pcb_outline(side="left");
        }
        if(location[4] == "trrs_right") {
          trrs_pcb_outline(side="right");
        }
        if(location[4] == "trrs") {
          trrs_pcb_outline(side="none");
        }
        if(location[4] == "proton_c") {
          proton_c_pcb_outline(size="full");
        }
        if(location[4] == "proton_c_short") {
          proton_c_pcb_outline(size="short");
        }
        if(location[4] == "ec11") {
          ec11_pcb_outline();
        }
        if(location[4] == "ec11_double") {
          ec11_pcb_outline();
        }
        if(location[4] == "mts_101") {
          mts_101_pcb_outline();
        }
        if(location[4] == "wire_12") {
          wire_pcb_outline(12);
        }
        if(location[4] == "wire_14") {
          wire_pcb_outline(14);
        }
        if(location[4] == "wire_10") {
          wire_pcb_outline(10);
        }
        if(location[4] == "wire_8") {
          wire_pcb_outline(8);
        }
        if(location[4] == "wire_16") {
          wire_pcb_outline(16);
        }
        if(location[4] == "support_2mm") {
          support_pcb_outline(2);
        }
        if(location[4] == "suppor_3mm") {
          support_pcb_outline(3);
        }
        if(location[4] == "support_4mm") {
          support_pcb_outline(4);
        }
        if(location[4] == "manual_trace") {
          assert(len(location[5]) > 0, "Manual trace must provide vector.");
          manual_trace_pcb_outline(locations[0]);
        }
      }
  }
}

module circuits_space_outline(locations) {
  if(len(locations) > 0) {
    circuits_space_outline(pop(locations));
    location = circuit_position(locations[0]);
    translate([location[0],location[1],location[2]]) 
      rotate(location[3]) {
        if(location[4] == "pro_micro") {
          pro_micro_space_outline();
        }
        if(location[4] == "trrs_left") {
          trrs_space_outline(side="left");
        }
        if(location[4] == "trrs_right") {
          trrs_space_outline(side="right");
        }
        if(location[4] == "trrs") {
          trrs_space_outline(side="none");
        }
        if(location[4] == "proton_c") {
          proton_c_space_outline(size="full");
        }
        if(location[4] == "proton_c_short") {
          proton_c_space_outline(size="short");
        }
        if(location[4] == "ec11") {
          ec11_space_outline();
        }
        if(location[4] == "ec11_double") {
          ec11_space_outline();
        }
        if(location[4] == "mts_101") {
          mts_101_space_outline();
        }
        if(location[4] == "wire_12") {
          wire_space_outline(12);
        }
        if(location[4] == "wire_14") {
          wire_space_outline(14);
        }
        if(location[4] == "wire_10") {
          wire_space_outline(10);
        }
        if(location[4] == "wire_8") {
          wire_space_outline(8);
        }
        if(location[4] == "wire_16") {
          wire_space_outline(16);
        }
        if(location[4] == "support_2mm") {
          support_space_outline(2);
        }
        if(location[4] == "support_3mm") {
          support_space_outline(3);
        }
        if(location[4] == "support_4mm") {
          support_space_outline(4);
        }
        if(location[4] == "manual_trace") {
          assert(len(location[5]) > 0, "Manual trace must provide vector.");
          manual_trace_space_outline(locations[0]);
        }
      }
  }
}
