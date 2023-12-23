function vdef(vector, index) = len(vector) == index ? vector[index-1] : vector[index];
function vadd(vector, index, axis) = vdef(vector, index)[axis] > vdef(vector, index-1)[axis] ? 0.01 : -0.01;
function polygon_from_vector(vector) = 
  len(vector) > 0 ?
    concat(vector, 
      [for (i = [1:len(vector)]) 
        [vector[len(vector)-i][0]-vadd(vector, i, 0),vector[len(vector)-i][1]-vadd(vector, i, 1)]])
      : [];

function parse_loc(loc) = [
  loc[5],
  len(loc) < 7 ? "both" : loc[6],
  len(loc) < 8 ? "none" : loc[7],
];

module manual_trace_pcb_drill(location) {
  vector = parse_loc(location)[0];
  echo("holes", parse_loc(location)[2]);
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_begin") {
    translate(vector[0]) {
      circle(d=1, $fn=20);
    }
  }
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_end") {
    translate(vector[len(vector)-1]) {
      circle(d=1, $fn=20);
    }
  }
}

module manual_trace_pcb_traces(location) {
  vector = parse_loc(location)[0];
  if(parse_loc(location)[1] != "bottom") {
    offset(0.4) {
      polygon(points=polygon_from_vector(vector));
    }
  }
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_begin") {
    translate(vector[0]) {
      circle(d=2.5, $fn=20);
    }
  }
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_end") {
    translate(vector[len(vector)-1]) {
      circle(d=2.5, $fn=20);
    }
  }
}

module manual_trace_pcb_traces_bottom(location) {
  vector = parse_loc(location)[0];
  if(parse_loc(location)[1] != "top") {
    offset(0.4) {
      polygon(points=polygon_from_vector(vector));
    }
  }
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_begin") {
    translate(vector[0]) {
      circle(d=2.5, $fn=20);
    }
  }
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_end") {
    translate(vector[len(vector)-1]) {
      circle(d=2.5, $fn=20);
    }
  }
}

module manual_trace_pcb_outline(location) {
  vector = parse_loc(location)[0];
  echo("location", location);
  offset(1)
    polygon(points=polygon_from_vector(vector));

  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_begin") {
    translate(vector[0]) {
      circle(d=4, $fn=20);
    }
  }
  if(parse_loc(location)[2] == "holes" || parse_loc(location)[2] == "hole_end") {
    translate(vector[len(vector)-1]) {
      circle(d=4, $fn=20);
    }
  }
}

module manual_trace_space_outline(location) {
  vector = parse_loc(location)[0];
  translate([0,0,-1])
    linear_extrude(2)
      offset(0.5)
        manual_trace_pcb_outline(vector);
}
