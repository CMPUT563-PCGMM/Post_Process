from os import listdir, getcwd
import numpy as np
import copy
import pickle
import random


def read_map_directory(map_directory):
    path_ = getcwd() + "\\" + map_directory
    files_ = listdir(path_)
    for i in range(len(files_)):
        files_[i] = map_directory + "\\" + files_[i]
    return files_


def read_file(file_name):
    first_list = []
    with open(file_name) as file:
        for line in file.readlines():
            second_list = []
            for j in line:
                if not j == '\n':
                    second_list.append(j)
            first_list.append(second_list)
    return np.array(first_list, dtype='str')


def extract_config(conf_height, conf_width, input_map):
    configs = []
    for i in range(1,input_map.shape[0] - conf_height):
        for j in range(1,input_map.shape[1] - conf_width):
            #print(input_map[i:i+conf_height, j:j+conf_width])
            configs.append(input_map[i:i+conf_height, j:j+conf_width])
    return configs


def replace_i_j(conf, i, j, symbol):
    conf_shape = conf.shape
    conf_copy = copy.deepcopy(conf)
    if i < conf_shape[0] and j < conf_shape[1]:
        conf_copy[i,j] = symbol
    return conf_copy


def conf_counter(dict, config):
    configs = conf_fliper(config)
    for c in configs:
        t = ()
        for i in range(len(c)):
            t = t + tuple(c[i])
        if t not in dict:
            dict[t] = 1
        else:
            dict[t] = dict[t] + 1


def conf_fliper(config):
    list_of_confs = []
    list_of_confs.append(config)
    temp = np.flip(config, 0)
    list_of_confs.append(temp)
    temp = np.flip(temp, 1)
    list_of_confs.append(temp)
    temp = np.flip(temp, 0)
    list_of_confs.append(temp)
    return list_of_confs


def all_confs(map_list, middle):
    dict = {}
    for each_map in map_list:
        map_array = read_file(each_map)
        confs = extract_config(3, 3, map_array)
        for each_config in confs:
            if middle:
                conf_counter(dict, each_config)
            else:
                conf_counter(dict, replace_i_j(each_config,1,1,'?'))
    return dict


def save_dict(dict, file_name):
    file = open(file_name + '.pickle', 'wb')
    pickle.dump(dict, file)


def load_dict(file_name):
    file = open(file_name, 'rb')
    return pickle.load(file)


def compare_configs(conf1, conf2):
    if conf1 == conf2:
        return len(conf1)
    else:
        return conf_intersection(conf1, conf2)


def conf_intersection(conf1, conf2):
    cntr = 0
    for i in range(len(conf1)):
        if conf1[i] == conf2[i]:
            cntr = cntr + 1
    return cntr


def convert_to_tuple(sample_config):
    t = ()
    for i in range(len(sample_config)):
        t = t + tuple(sample_config[i])
    return t


def configs_converter(list_of_confs):
    for i in range(len(list_of_confs)):
        list_of_confs[i] = convert_to_tuple(list_of_confs[i])
    return list_of_confs


def check_conf(config, first_dict, second_dict):
    new_dict = {}
    if config not in first_dict:
        conf_surrounding = replace_tuple_middle(config, '?')
        if conf_surrounding in second_dict:
            new_dict[conf_surrounding] = compare_configs(conf_surrounding, conf_surrounding)
        else:
            for key in second_dict:
                cnt = compare_configs(key, conf_surrounding)
                if cnt > 0:
                    new_dict[key] = cnt
    return new_dict


def replace_tuple_middle(inp, symbol):
    new_tuple = ()
    middle = 0.5 * (len(inp) - 1)
    for i in range(len(inp)):
        if i == middle:
            new_tuple = new_tuple + tuple(symbol)
        else:
            new_tuple = new_tuple + tuple(inp[i])
    return new_tuple


def find_dict_max(sample_dict):
    keys = []
    max_key = max(sample_dict, key=sample_dict.get)
    max_val = sample_dict[max_key]
    for key in sample_dict:
        if sample_dict[key] == max_val:
            keys.append(key)
    return keys


def find_configs(max_keys, over_lap_cnt, first_dict):
    list_of_desired_confs = []
    for each_max_key in max_keys:
        for each_key in first_dict:
            if compare_configs(each_key, each_max_key) == over_lap_cnt:
                list_of_desired_confs.append(each_key)
    return list_of_desired_confs


def generate_new_tile(list_of_desired_configs, ref_dict):
    temp_conf_list = []
    temp_conf_cnt = []
    s = 0
    for k in list_of_desired_configs:
        s = s + ref_dict[k]
        temp_conf_cnt.append(s)
        temp_conf_list.append(k)
    r = random.randint(1, s)
    for i in range(len(temp_conf_cnt) - 1):
        if r > temp_conf_cnt[i] and r <= temp_conf_cnt[i+1]:
            return temp_conf_list[i+1]
        else:
            return temp_conf_list[i]


def handel_the_map(configs, dict1, dict2):
    new_dict = check_conf(configs, dict1, dict2)
    if len(new_dict) > 0:
        max_overlap_keys = find_dict_max(new_dict)
        max_overlap_num = new_dict[max_overlap_keys[0]]
        if max_overlap_num == 9:
            max_overlap_num = 8
        desired_confs = find_configs(max_overlap_keys, max_overlap_num, dict1)
        if len(desired_confs) == 1:
            new_tile = desired_confs[0]
        else:
            new_tile = generate_new_tile(desired_confs, dict1)
    #    print(new_tile)
        return new_tile
    else:
        return configs


def extract_config_update(conf_height, conf_width, input_map, dict1, dict2):
    temp = copy.deepcopy(input_map)
    for i in range(1,input_map.shape[0] - conf_height):
        for j in range(1,input_map.shape[1] - conf_width):
            sample_conf = configs_converter([input_map[i:i+conf_height, j:j+conf_width]])
            tile_to_replace = handel_the_map(sample_conf[0], dict1, dict2)[4]
            if not (tile_to_replace == sample_conf[0][4]):
                temp[i+1, j+1] = tile_to_replace
    return temp
            #temp[i+1, j+1] = tile_to_replace
            #print(tile_to_replace == sample_conf[0][4])


def iterate_over_map(iteration, conf_height, conf_width, input_map, dict1, dict2):
    print(input_map[2])
    for i in range(iteration):
        new_map = extract_config_update(conf_height, conf_width, input_map, dict1, dict2)
        print(new_map[2])
        if check_equality(new_map, input_map):
            print(i)
            break
        input_map = new_map
    return input_map

            #input_map[i+1, j+1] = tile_to_replace
            #handel_the_map(configs_converter(input_map[i:i+conf_height, j:j+conf_width])[0], dict1, dict2)

def check_equality(map1, map2):
    for i in range(map1.shape[0]):
        for j in range(map1.shape[1]):
            if map1[i][j] != map2[i][j]:
                return False
    return True