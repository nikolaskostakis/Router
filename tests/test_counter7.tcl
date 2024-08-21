## Test for design counter7
## Filepath is written for execution on Windows
read_design -f benchmarks\\counter7.txt
# place_random
# save_components_coords -f data\\counter7.txt
load_components_coords -f data\\counter7.txt
#create_bins -size 10 10
create_bins -size 3 3
#add_blockage -bin 7 5
#list_components
#list_io_ports
#list_nets
#maze_routing 
maze_routing -startRoutingFromCenter
#maze_routing_net N3
#bins_info
net_info N15
#calculate_WL -HPWL
#calculate_WL -tree
start_gui
quit