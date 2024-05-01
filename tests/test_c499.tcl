read_design -f benchmarks\\c499.practicalformat.txt
# place_random
# save_components_coords -f data\\c499.txt
load_components_coords -f data\\c499.txt
create_bins -size 10 10
add_blockage -bin 3 3
add_blockage -bin 3 4
#
list_components
list_io_ports
list_nets
#
#maze_routing -counterclockwise
maze_routing
#net_info N16
start_gui
net_info N21
exit