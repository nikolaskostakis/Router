read_design -f benchmarks\\alu.txt
#place_random 
#save_components_coords -f data\\alu.txt
load_components_coords -f data\\alu.txt
create_bins -size 14 14
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit