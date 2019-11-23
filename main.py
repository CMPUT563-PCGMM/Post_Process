from functions import *


#map_directory = "maps"
#maps_list = read_map_directory(map_directory)
#dict = all_confs(maps_list, True)
#save_dict(dict, '3by3_conifg_with_middle')


dict1 = load_dict('3by3_conifg_with_middle.pickle')
dict2 = load_dict('3by3_conifg_with_out_middle.pickle')



sample_map = read_file("unplayable_tloz9_2_room_6.txt")
#print(sample_map)
#configs = extract_config(3, 3, sample_map)
#configs = configs_converter(configs)
#for i in configs:
    #pass
#    print(i)
#print(configs[3])
#handel_the_map(configs[4], dict1, dict2)
#for i in range(len(configs)):
#    print(handel_the_map(configs[i], dict1, dict2))
#print(sample_map)
new_map = iterate_over_map(1000, 3, 3, sample_map, dict1, dict2)
#print(new_map[2])
'''
new_dict = check_conf(configs[0], dict1, dict2)
max_overlap_keys = find_dict_max(new_dict)
max_overlap_num = new_dict[max_overlap_keys[0]]
desired_confs = find_configs(max_overlap_keys, 8, dict1)
selected_conf = generate_new_tile(desired_confs, dict1)
print(selected_conf)
'''