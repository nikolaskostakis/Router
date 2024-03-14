read_design -f benchmarks\\c499.practicalformat.txt
# place_random
# save_components_coords -f data\\c499.txt
load_components_coords -f data\\c499.txt
create_bins -size 10 10
#
list_components
list_io_ports
#
#maze_routing -counterclockwise
maze_routing
net_info N16
start_gui
exit