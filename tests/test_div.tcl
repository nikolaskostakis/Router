read_design -f benchmarks\\div.txt
# place_random -tries 200_000
# save_components_coords -f data\\div.txt
load_components_coords -f data\\div.txt
create_bins -size 11 11
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing
start_gui
exit