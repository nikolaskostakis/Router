read_design -f benchmarks\\c17.practicalformat.txt
# list_components
place_random
# save_components_coords -f data\\c17.txt
load_components_coords -f data\\c17.txt
create_bins -size 5 5
maze_routing
start_gui
exit