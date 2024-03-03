## Test for design counter7
## Filepath is written for execution on Windows
read_design -f benchmarks\\counter7.txt
# place_random
# save_components_coords -f data\\counter7.txt
load_components_coords -f data\\counter7.txt
create_bins -size 10 10
maze_routing
bins_info
calculate_WL -HPWL
calculate_WL -tree
start_gui
quit