read_design -f benchmarks\\c6288.practicalformat.txt
# place_random
# save_components_coords -f data\\c6288.txt
load_components_coords -f data\\c6288.txt
create_bins -size 35 35
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit