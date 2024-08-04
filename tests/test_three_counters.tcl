read_design -f benchmarks\\three_counters.practicalformat.txt
place_random
# save_components_coords -f data\\three_counters.txt
# load_components_coords -f data\\three_counters.txt
create_bins -size 11 11
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit