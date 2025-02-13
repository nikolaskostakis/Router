read_design -f benchmarks\\c499.practicalformat.txt
# place_random
# save_components_coords -f data\\c499.txt
load_components_coords -f data\\c499.txt
create_bins -size 13 13
#create_bins -size 10 10
add_blockage -bin 5 6
#add_blockage -bin 3 4
#
#maze_routing -counterclockwise
maze_routing  -counterclockwise
#net_info N16
calculate_WL -HPWL
calculate_WL -tree
start_gui
exit