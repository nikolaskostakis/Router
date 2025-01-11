read_design -f benchmarks\\c1908.practicalformat.txt
# place_random
# save_components_coords -f data\\c1908.txt
load_components_coords -f data\\c1908.txt
#create_bins -size 14 14
create_bins -size 28 28
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing  -counterclockwise
calculate_WL -HPWL
calculate_WL -tree
start_gui
exit