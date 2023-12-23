use <../../../lib/circuits/ec11.scad>

module ec11_test(single=true, connections=["hole","hole","hole","hole"]){
  difference(){
    union(){
      linear_extrude(0.5)
        projection()
          ec11_space_outline();
      translate([0,0,-0.1])
        color("green")
          linear_extrude(1)
            ec11_pcb_outline();
      translate([0,0,0.4])
        color("red")
          linear_extrude(1.1)
            ec11_pcb_traces(single=single, connections=connections);
      if(!single)
        translate([0,0,-1])
          color("purple")
            linear_extrude(1.1)
              ec11_pcb_traces_bottom(connections=connections);
    }
    translate([0,0,-2])
      linear_extrude(5)
        ec11_pcb_drill(single=single, connections=connections);
  }
}

ec11_test();

translate([22,0]) {
  ec11_space_outline();
}

translate([0,22]){
  ec11_test(single=false);
}

translate([0,44]){
  ec11_test(single=false, connections=["connect","connect","connect","connect"]);
}

translate([0,66]){
  ec11_test(single=false, connections=["none","none","none","none"]);
}

translate([0,-22]){
  ec11_test(single=true, connections=["none","none","none","none"]);
}