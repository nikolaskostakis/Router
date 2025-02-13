read_design -f benchmarks\\c5315.practicalformat.txt
# place_random
# save_components_coords -f data\\c5315.txt
load_components_coords -f data\\c5315.txt
#create_bins -size 25 25
create_bins -size 50 50
add_blockage -bin 16 23
add_blockage -bin 18 25
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing -counterclockwise
start_gui
calculate_WL -HPWL
calculate_WL -tree
exit