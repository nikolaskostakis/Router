read_design -f benchmarks\\c1908.practicalformat.txt
# place_random
# save_components_coords -f data\\c1908.txt
load_components_coords -f data\\c1908.txt
create_bins -size 14 14
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit