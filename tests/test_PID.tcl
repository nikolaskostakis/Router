read_design -f benchmarks\\PID.practicalformat.txt
# place_random 
# save_components_coords -f data\\PID.txt
load_components_coords -f data\\PID.txt
create_bins -size 64 64
add_blockage -bin 31 43
add_blockage -bin 42 27
add_blockage -bin 25 19
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
calculate_WL -HPWL
calculate_WL -tree
exit