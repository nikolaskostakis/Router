read_design -f benchmarks\\execute.txt
#place_random 
#save_components_coords -f data\\execute.txt
load_components_coords -f data\\execute.txt
create_bins -size 94 94
add_blockage -bin 40 58
add_blockage -bin 16 37
add_blockage -bin 67 35
net_info N1
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing  -counterclockwise
start_gui
calculate_WL -HPWL
calculate_WL -tree
exit