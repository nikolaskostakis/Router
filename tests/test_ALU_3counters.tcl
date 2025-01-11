read_design -f benchmarks\\ALU_3counters.txt
# place_random
# save_components_coords -f data\\ALU_3counters.txt
load_components_coords -f data\\ALU_3counters.txt
# calculate_WL -HPWL
# calculate_WL -tree
create_bins -size 16 16
#create_bins -size 7 7
#add_blockage -bin 2 3
maze_routing -counterclockwise
calculate_WL -HPWL
calculate_WL -tree
start_gui
quit