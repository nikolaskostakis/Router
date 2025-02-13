read_design -f benchmarks\\c1355.practicalformat.txt
# place_random
# save_components_coords -f data\\c1355.txt
load_components_coords -f data\\c1355.txt
create_bins -size 13 13
add_blockage -bin 8 6
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing  -counterclockwise
calculate_WL -HPWL
calculate_WL -tree
start_gui
exit