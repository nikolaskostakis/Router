read_design -f benchmarks\\PID.practicalformat.txt
# place_random 
# save_components_coords -f data\\PID.txt
load_components_coords -f data\\PID.txt
create_bins -size 16 16
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit