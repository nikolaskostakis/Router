read_design -f benchmarks\\c432.practicalformat.txt
# place_random
# save_components_coords -f data\\c432.txt
load_components_coords -f data\\c432.txt
create_bins -size 18 18
#create_bins -size 13 13
#add_blockage -bin 3 3
#add_blockage -bin 3 4
#
#list_components
#list_io_ports
#list_nets
#
add_blockage -bin 6 8
#maze_routing -counterclockwise
maze_routing  
#net_info N16
calculate_WL -HPWL
calculate_WL -tree
design_info
start_gui
exit