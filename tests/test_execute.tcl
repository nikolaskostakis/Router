read_design -f benchmarks\\execute.txt
place_random 
save_components_coords -f data\\execute.txt
#load_components_coords -f data\\execute.txt
create_bins -size 14 14
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit