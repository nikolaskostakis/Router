read_design -f benchmarks\\ALU_3counters.txt
# place_random
# save_components_coords -f data\\ALU_3counters.txt
load_components_coords -f data\\ALU_3counters.txt
# calculate_WL -HPWL
# calculate_WL -tree
create_bins -size 5 5
maze_routing
start_gui
quit