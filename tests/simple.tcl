read_design -f benchmarks\\counter7.txt
# place_random
# save_components_coords -f data\\counter7.txt
load_components_coords -f data\\counter7.txt
create_bins -size 8 8
list_nets
list_io_ports
#start_gui
#quit
#maze_routing
bins_info
quit