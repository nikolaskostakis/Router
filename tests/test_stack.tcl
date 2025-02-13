read_design -f benchmarks\\stack.txt
place_random 
save_components_coords -f data\\stack.txt
#load_components_coords -f data\\stack.txt
create_bins -size 38 38
add_blockage -bin 18 13
add_blockage -bin 14 9
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing -counterclockwise
start_gui
calculate_WL -HPWL
calculate_WL -tree
exit