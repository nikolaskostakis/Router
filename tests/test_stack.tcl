read_design -f benchmarks\\stack.txt
place_random 
save_components_coords -f data\\stack.txt
#load_components_coords -f data\\stack.txt
create_bins -size 5 5
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit