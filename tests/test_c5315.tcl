read_design -f benchmarks\\c5315.practicalformat.txt
# place_random
# save_components_coords -f data\\c5315.txt
load_components_coords -f data\\c5315.txt
create_bins -size 25 25
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit