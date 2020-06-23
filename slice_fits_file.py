# -*- coding: utf-8 -*-

import fitsio
import numpy as np
import argparse
import os
import glob
import pprint
import yaml
import pandas as pd

def correct_endianness(input_data, needed_endianness):
    return input_data.byteswap().newbyteorder(needed_endianness)

class Filter:
    @staticmethod
    def filter_data_by_crit(input_data, criteria_min, criteria_max):
        # Criteria is a dictionary with col name and val limit
        
        # input_data_native_endian = correct_endianness(input_data, '=')
        # df = pd.DataFrame(input_data_native_endian)

        # for col_name, min_value in criteria_min.items():
        #     indexes_to_drop = df[df[col_name] < min_value].index
        #     df.drop(indexes_to_drop, inplace=True)
 
        # for col_name in criteria_max:
        #     df.drop(df[df[col_name] > criteria_max[col_name]].index, inplace=True)

        for col_name, min_value in criteria_min.items():
            input_data = input_data[input_data[col_name] < min_value]
        
        for col_name, max_value in criteria_max.items():
            input_data = input_data[input_data[col_name] > max_value]
        
        return input_data

    @staticmethod
    def filter_data_by_index(input_data, indexes_to_remove, index_col_name):

        col_filter = np.in1d(input_data[index_col_name], indexes_to_remove, assume_unique=True)

        output_data = input_data[col_filter]

        return output_data
    

class Catalog:

    def slice_gal(self, fits_in, fits_out , criteria_min=None, criteria_max=None):
        # Criteria is a dictionary with col name and val limit
        input_data = None

        print(f' fits_in = {fits_in}')
        print(f' fits_out = {fits_out}')
        print(f' criteria_min = {criteria_min}')
        print(f' criteria_max = {criteria_max}')
    

        input_data = fitsio.read(fits_in)
        if self.older_sister_name is not None:
            self.indexes_to_remove = self.sister_catalog.indexes_to_remove
            input_data = Filter.filter_data_by_index(input_data, self.indexes_to_remove, self.own_index_name)
        else:
            input_data = Filter.filter_data_by_crit(input_data, criteria_min, criteria_max)
            self.indexes_to_remove = input_data[self.own_index_name]

        fitsio.write(fits_out, input_data)

        return None

    def slice_catalog(self):
        print(f'{self.name} in: ')

        for cat_in, cat_out in self.cats.items():
            pp.pprint(cat_in)
            self.slice_gal(cat_in, cat_out, self.lower_right_apex, self.upper_left_apex)
            pp.pprint(cat_out)

        print(f'{self.name} out: ')

    def parse_configuration(self):
        #  TODO: Check names
        self.lower_right_apex ={** self.conf['LOWER_RIGHT_APEX'][0], ** self.conf['LOWER_RIGHT_APEX'][1]}
        self.upper_left_apex = {** self.conf['UPPER_LEFT_APEX'][0], ** self.conf['UPPER_LEFT_APEX'][1]}
        print(f'criteria_min: {self.lower_right_apex}, criteria_max: {self.upper_left_apex}') 

        try:
            siblings = self.conf['JOIN_FROM']
            
            for sister in siblings:
                sister_name = list(sister)[0]
                if sister_name != self.name:
                    self.older_sister_name.append(sister_name)
                    self.siblings_name.append(sister[sister_name])
                else:
                    self.own_index_name = sister[self.name]
        except KeyError:
            self.older_sister_name = None

        try:
            siblings = self.conf['JOIN_TO']

            for sister in siblings:
                sister_name = list(sister)[0]
                if sister_name != self.name:
                    self.little_sister_name.append(sister_name)
                    self.siblings_name.append(sister[sister_name])
                else:
                    self.own_index_name = sister[self.name]

        except KeyError:
            self.little_sister_name = None
    

    @staticmethod
    def inner_join(ref_file, coords_file, file_out):

        return None
    
    def meet_sister(self, sister_instance):
        self.sister_catalog = sister_instance
    
    
    def __init__(self, cat_name, configuration, cats):
        self.index_name = None
        self.index_to_keep = None
        self.sister_catalog = None
        self.little_sister_name = [] 
        self.older_sister_name = []
        self.name = file_information
        self.conf = configuration 
        self.cats = cats
        self.own_index_name = None 
        self.siblings_name = []

        self.parse_configuration() 


class Paths:
    @staticmethod
    def get_fullpath(path):
        return glob.glob(os.path.abspath(path))

    @staticmethod
    def get_dir_out(input_outdir, prefix):
        import pdb; pdb.set_trace
        try:
            os.makedirs(input_outdir, exist_ok=True)
        except TypeError:
            input_outdir = os.path.join(os.getcwd(), prefix + '_fits_slices')
            os.makedirs(input_outdir, exist_ok=True)
            
        dir_out = Paths.get_fullpath(input_outdir)[0]

        return dir_out


    @staticmethod
    def get_outpath(fullpath_in, dir_out, prefix):
        basename = os.path.basename(fullpath_in)
        output_filepath = os.path.join(dir_out, prefix + '_' + basename)

        return output_filepath


def read_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--conf', help='Path of configuration file', type=str)
    arg_parser.add_argument('-o', '--output', help='Path of output dir', type=str)
    args = arg_parser.parse_args()

    return args

def cats_files(filepath, dir_out, prefix):
    cats_in = Paths.get_fullpath(filepath)

    cats_files = {}
    for cat in cats_in:
        cats_files[cat] = Paths.get_outpath(cat, dir_out, prefix)

    return cats_files


if __name__ == "__main__":

    args = read_args()
    pp = pprint.PrettyPrinter(indent=4)
    
    prefix = '10sqdeg'
    conf_file = args.conf  
    dir_out = Paths.get_dir_out(args.output, prefix)

    with open(conf_file, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    cat_list = {}

    for file_information in conf:
        cats = cats_files(conf[file_information]['FILEPATH'], dir_out, prefix)
        cat_list[file_information] = Catalog(file_information, conf[file_information], cats)

    for cat_name, cat_instance in cat_list.items():
        if cat_instance.little_sister_name:
            cat_instance.meet_sister(cat_list[cat_instance.little_sister_name[0]])
        elif cat_instance.older_sister_name:
            cat_instance.meet_sister(cat_list[cat_instance.older_sister_name[0]])

    for cat_name, cat_instance in cat_list.items():
        print(f'Cat name: {cat_name}')
        cat_instance.slice_catalog()
