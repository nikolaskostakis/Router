read_design -f benchmarks\\c3540.practicalformat.txt
# place_random
# save_components_coords -f data\\c3540.txt
load_components_coords -f data\\c3540.txt
create_bins -size 23 23
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit