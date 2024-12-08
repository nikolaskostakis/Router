read_design -f benchmarks\\c17.practicalformat.txt
# list_components
place_random
# save_components_coords -f data\\c17.txt
load_components_coords -f data\\c17.txt
create_bins -size 3 3
net_info N3
#maze_routing -counterclockwise
maze_routing 
net_info N3
start_gui
save_design -f c17.pickle
list_io_ports
exit