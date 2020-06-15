import fitsio
import numpy as np
import argparse
import os
import glob
import pprint

def delete_where(input_data, filters):

    # Criteria is a dictionary with col name and val limit

    filtered_data = np.delete(input_data, filters)

    return filtered_data

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

    filter_min_ra = np.where(input_data['ra_gal'] < criteria_min['ra_gal'])
    filter_max_ra = np.where(input_data['ra_gal'] > criteria_max['ra_gal'])
    filter_min_dec = np.where(input_data['dec_gal'] < criteria_min['dec_gal'])
    filter_max_dec = np.where(input_data['dec_gal'] > criteria_max['dec_gal'])

    filters = np.concatenate((filter_min_ra, filter_max_ra, filter_min_dec, filter_max_dec), axis=None)
    filters = np.unique(filters)
    input_data = delete_where(input_data, filters)

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
    arg_parser.add_argument('-G', '--gal', help='Path of galaxies_file', type=str)
    arg_parser.add_argument('-P', '--phz', help='Path of photo_z fileS', type=str)
    arg_parser.add_argument('-M', '--matching', help='Path of matching files', type=str)
    arg_parser.add_argument('-O', '--output', help='Output_dir', type=str)
    arg_parser.add_argument('--ra_min', help='RA min', type=float)
    arg_parser.add_argument('--ra_max', help='RA max', type=float)
    arg_parser.add_argument('--dec_min', help='Dec min', type=float)
    arg_parser.add_argument('--dec_max', help='Dec max', type=float)
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

if __name__ == "__main__":
    args = read_args()
    pp = pprint.PrettyPrinter(indent=4)
    ra_min = args.ra_min
    ra_max = args.ra_max
    dec_min = args.dec_min
    dec_max = args.dec_max

    print(f'Interval RA:{ra_min}-{ra_max}, Interval Dec:{dec_min}-{dec_max}')
    if not ra_min or not ra_max or not dec_min or not dec_max:
        raise AttributError(f'Missing parameter')

    criteria_min = {'ra_gal':ra_min, 'dec_gal':dec_min}
    criteria_max = {'ra_gal':ra_max, 'dec_gal':dec_max}

    print(f'criteria_min: {criteria_min}, criteria_max: {criteria_max}')

    gal_in = get_fullpath(args.gal)
    phz_in = get_fullpath(args.phz)
    matching_in = get_fullpath(args.matching)

    prefix = '10sqdeg'
    dir_out = get_dir_out(args.output, prefix)
    gal_out = get_outpath(gal_in, dir_out, prefix)
    phz_out = get_outpath(phz_in, dir_out, prefix)
    matching_out = get_outpath(matching_in, dir_out, prefix)

    print(f'Gal in: ')
    pp.pprint(gal_in)
    slice_gal(gal_in, gal_out, criteria_min, criteria_max)
    print(f'Gal out: ')
    pp.pprint(gal_out)
    
    print(f'PHZ in: ')
    pp.pprint(phz_in)
    slice_gal(phz_in, phz_out, criteria_min, criteria_max)
    print(f'PHZ out: ')
    pp.pprint(phz_out)
    
    print('Matching in: ')
    pp.pprint(matching_in)
    slice_gal(matching_in, matching_out, criteria_min, criteria_max)
    print('Matching out: ')
    pp.pprint(matching_out)
