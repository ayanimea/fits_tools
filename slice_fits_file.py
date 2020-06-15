# -*- coding: utf-8 -*-

import fitsio
import numpy as np
import argparse
import os
import glob
import pprint
import yaml

def delete_where(input_data, filters):

    # Criteria is a dictionary with col name and val limit
    filtered_data = np.delete(input_data, filters)

    return filtered_data

def filter_data(input_data, criteria_min, criteria_max):
    filter_min_ra = np.where(input_data['ra_gal'] < criteria_min['ra_gal'])
    filter_max_ra = np.where(input_data['ra_gal'] > criteria_max['ra_gal'])
    filter_min_dec = np.where(input_data['dec_gal'] < criteria_min['dec_gal'])
    filter_max_dec = np.where(input_data['dec_gal'] > criteria_max['dec_gal'])

    filters = np.concatenate((filter_min_ra, filter_max_ra, filter_min_dec, filter_max_dec), axis=None)

    filters = np.unique(filters)
    input_data = delete_where(input_data, filters)
    return input_data

def slice_gal(fits_in, fits_out , criteria_min, criteria_max):
    # Criteria is a dictionary with col name and val limit

    input_data = None

    print(f' fits_in = {fits_in}')
    
    for each_datafile in fits_in:
        data = fitsio.read(each_datafile)
        if input_data is None:
            input_data = data
        else:
            input_data = np.concatenate((input_data, data))

    input_data = filter_data(input_data, criteria_min, criteria_max)

    fitsio.write(fits_out, input_data)

def slices_mass_redshift(matching_in, matching_out, criteria_min):
    matching = fitsio.read(matching_in)

    filter_min_mass = np.where(matching['H_MASS'] < criteria_min['H_MASS'])
    filter_min_redshift = np.where(matching['C_Z'] < criteria_min['C_Z'])
    filter_min_match = np.where(matching['MATCH'] == criteria_min['MATCH'])
    filters = np.concatenate((filter_min_mass, filter_min_redshift, filter_min_match), axis=None)
    matching = np.delete(matching, filters)

    fitsio.write(matching_out, matching)

def read_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--conf', help='Path of configuration file', type=str)
    arg_parser.add_argument('-o', '--output', help='Path of output dir', type=str)
    args = arg_parser.parse_args()

    return args

def get_fullpath(path):
    try:
        fullpath = glob.glob(os.path.abspath(path))
    except TypeError:
        fullpath = []

    return fullpath

def get_dir_out(input_outdir, prefix):
    try:
        dir_out = get_fullpath(input_outdir)[0]
    except IndexError:
        dir_out = os.path.join(os.getcwd(), prefix + '_fits_slices')

        try:
            os.mkdir(dir_out)
            print("Directory " , dir_out ,  "created.") 
        except FileExistsError:
            print("Directory " , dir_out ,  " already exists.")

    return dir_out


def get_outpath(fullpath_in, dir_out, prefix):

    try:
        first_file =  sorted(fullpath_in, key=str.lower)[0]
        basename = os.path.basename(first_file)
        output_filepath = os.path.join(dir_out, prefix + '_' + basename)
    except IndexError:
        output_filepath = None

    return output_filepath

def slice_catalog(file_information, conf, dir_out, prefix):
    cat_in = get_fullpath(conf['FILEPATH'])
    
    # TODO: Check names
    lower_right_apex = conf['LOWER_RIGHT_APEX']
    upper_left_apex = conf['UPPER_LEFT_APEX']
    
    print(f'criteria_min: {lower_right_apex}, criteria_max: {upper_left_apex}') 
    cat_out = get_outpath(cat_in, dir_out, prefix)
    print(f'{file_information} in: ')
    pp.pprint(cat_in)
    slice_gal(cat_in, cat_out, lower_right_apex, upper_left_apex)
    print(f'{file_information} out: ')
    pp.pprint(cat_out)
    


if __name__ == "__main__":
    args = read_args()
    pp = pprint.PrettyPrinter(indent=4)
    
    prefix = '10sqdeg'
    conf_file = args.conf    
    dir_out = get_dir_out(args.output, prefix)
    with open(conf_file, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    for file_information in conf:
        print(file_information)
        print(conf[file_information])
        slice_catalog(file_information, conf[file_information], dir_out, prefix)
