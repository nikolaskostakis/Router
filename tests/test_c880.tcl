read_design -f benchmarks\\c880.practicalformat.txt
#place_random
#save_components_coords -f data\\c880.txt
load_components_coords -f data\\c880.txt
#create_bins -size 13 13
create_bins -size 26 26
add_blockage -bin 7 13
add_blockage -bin 17 13
#
#list_components
#list_io_ports
#list_nets
#
#maze_routing -counterclockwise
maze_routing -counterclockwise
calculate_WL -HPWL
calculate_WL -tree
start_gui
exit