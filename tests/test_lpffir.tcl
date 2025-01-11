read_design -f benchmarks\\lpffir.practicalformat.txt
place_random 
save_components_coords -f data\\lpffir.txt
#load_components_coords -f data\\lpffir.txt
create_bins -size 25 25
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing  -counterclockwise
start_gui
calculate_WL -HPWL
calculate_WL -tree
exit