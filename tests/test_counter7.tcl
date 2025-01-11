## Test for design counter7
## Filepath is written for execution on Windows
read_design -f benchmarks\\counter7.txt
# place_random
# save_components_coords -f data\\counter7.txt
load_components_coords -f data\\counter7.txt
#create_bins -size 10 10
create_bins -size 9 9
#create_bins -size 5 5
add_blockage -bin 3 2
#list_components
#list_io_ports
#list_nets
#maze_routing -counterclockwise
maze_routing_net N18 -counterclockwise
#maze_routing_net N3
#bins_info
#calculate_WL -HPWL
#calculate_WL -tree
#list_nets
net_info N18
start_gui
quit