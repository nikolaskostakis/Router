#read_design -f benchmarks\\counter7.txt
#read_design -f benchmarks\\execute.txt
#place_random
# save_components_coords -f data\\counter7.txt
#load_components_coords -f data\\counter7.txt
#create_bins -size 8 8
# net_info N17
# list_nets
# list_io_ports
# quit
#maze_routing -counterclockwise
#net_info N17
#calculate_net_WL -net N17 -HPWL
#calculate_net_WL -net N17 -tree
#start_gui
#bins_info
#calculate_WL -HPWL
#calculate_WL -tree
#quit
load_design -f data\\c17.pickle
test
show_heatmap -all
bins_info
start_gui
exit

bins_info
net_info N5
net_info N8
net_info N9
list_nets
start_gui
exit