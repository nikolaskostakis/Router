read_design -f benchmarks\\c17.practicalformat.txt
# list_components
# start_gui
place_random
# save_components_coords -f data\\c17.txt
load_components_coords -f data\\c17.txt
create_bins -size 4 4
#net_info N3
#maze_routing -counterclockwise
add_blockage -bin 2 2
maze_routing  -counterclockwise
#net_info N3
start_gui
#save_design -f data\\c17.pickle
#list_io_ports
calculate_WL -HPWL
calculate_WL -tree
design_info
exit