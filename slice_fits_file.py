# -*- coding: utf-8 -*-

import fitsio
import numpy as np
import argparse
import os
import glob
import pprint
import yaml
class Filter:
    @staticmethod
    def delete_where(input_data, filters):

        # Criteria is a dictionary with col name and val limit
        filtered_data = np.delete(input_data, filters)

        return filtered_data

    @staticmethod
    def filter_data(fits_in, fits_out, criteria_min, criteria_max):
        filters = None

        input_data = fitsio.read(fits_in)

        for col_name in criteria_min:
            filters_min = np.where(input_data[col_name] < criteria_min[col_name])
            if filters is None:
                filters = np.copy(filters_min)
            else:
                filters = np.concatenate((filters, filters_min), axis=None)
        
        for col_name in criteria_max:
            filters_max = np.where(input_data[col_name] > criteria_max[col_name])
            if filters is None:
                filters = np.copy(filters_min)
            else:
                filters = np.concatenate((filters, filters_max), axis=None)
        
            print(filters)

        filters = np.unique(filters)
        print(f'filters: {filters}')
    
        fitsio.write(fits_out, input_data)

        return input_data

class Catalog:
    @staticmethod
    def slice_gal(fits_in, fits_out , criteria_min=None, criteria_max=None):
        # Criteria is a dictionary with col name and val limit
        input_data = None

        print(f' fits_in = {fits_in}')
        print(f' fits_out = {fits_out}')
        print(f' criteria_min = {criteria_min}')
        print(f' criteria_max = {criteria_max}')
    
        for each_datafile in fits_in:
            input_data = Filter.filter_data(each_datafile, fits_out, criteria_min, criteria_max)

        return None

    @staticmethod
    def slice_catalog(file_information, conf, dir_out, prefix):
        cat_in = Paths.get_fullpath(conf['FILEPATH'])
    
        #  TODO: Check names
        lower_right_apex ={** conf['LOWER_RIGHT_APEX'][0], ** conf['LOWER_RIGHT_APEX'][1]}
        upper_left_apex = {** conf['UPPER_LEFT_APEX'][0], ** conf['UPPER_LEFT_APEX'][1]}

        # Add index slice 
        print(f'criteria_min: {lower_right_apex}, criteria_max: {upper_left_apex}') 
        cat_out = Paths.get_outpath(cat_in, dir_out, prefix)
        print(f'{file_information} in: ')
        pp.pprint(cat_in)
        Catalog.slice_gal(cat_in, cat_out, lower_right_apex, upper_left_apex)

        print(f'{file_information} out: ')
        pp.pprint(cat_out)

    @staticmethod
    def inner_join(ref_file, coords_file, file_out):

        return None

class Paths:
    @staticmethod
    def get_fullpath(path):
        try:
            fullpath = glob.glob(os.path.abspath(path))
        except TypeError:
            fullpath = []

        return fullpath

    @staticmethod
    def get_dir_out(input_outdir, prefix):
        try:
            dir_out = Paths.get_fullpath(input_outdir)[0]
        except IndexError:
            dir_out = os.path.join(os.getcwd(), prefix + '_fits_slices')

            try:
                os.mkdir(dir_out)
                print("Directory " , dir_out ,  "created.") 
            except FileExistsError:
                print("Directory " , dir_out ,  " already exists.")

        return dir_out


    @staticmethod
    def get_outpath(fullpath_in, dir_out, prefix):
        try:
            first_file =  sorted(fullpath_in, key=str.lower)[0]
            basename = os.path.basename(first_file)
            output_filepath = os.path.join(dir_out, prefix + '_' + basename)
        except IndexError:
            output_filepath = None

        return output_filepath


def read_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--conf', help='Path of configuration file', type=str)
    arg_parser.add_argument('-o', '--output', help='Path of output dir', type=str)
    args = arg_parser.parse_args()

    return args


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

    for file_information in conf:
        Catalog.slice_catalog(file_information, conf[file_information], dir_out, prefix)
