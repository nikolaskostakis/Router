read_design -f benchmarks\\c7552.practicalformat.txt
# place_random
# save_components_coords -f data\\c7552.txt
load_components_coords -f data\\c7552.txt
create_bins -size 56 56
#create_bins -size 28 28
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing -counterclockwise
start_gui
calculate_WL -HPWL
calculate_WL -tree
exit