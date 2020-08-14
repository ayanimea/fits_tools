import fitsio
import numpy as np
import os
import pandas as pd

def generate_vector(length, num_type, mini, maxi):

    if num_type is 'float':
        new_vector = np.random.rand(length) * (maxi - mini) + mini
    elif num_type is 'int':
        new_vector = np.random.random_integers(mini, maxi, length)        

    return new_vector

def gen_amico_header(ra, dec, z):
    header = {'COORDSYS': 'SPHERICAL',
              'DET_CODE': 'AMICO',
              'MIN_Z': z['min'],
              'MAX_Z': z['max'],
              'SNR_THR': 3.0,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max'],
              'OMEGA_MAT': .25,
              'OMEGA_VAC': .75,
              'HUBBLE_PAR': 73,
              'W_EQ_STATE': -1,
              'N_EFF': 3.04,
              'TEMP_CMB': 0, 
              'CUBE_XY_STEP': 5,
              'MAX_AREA_DEG': 40,
              'L_BORDER_DEG': 0.1} 
    return header

def gen_pzwav_header(ra, dec, z):
    header = {'COORDSYS': 'SPHERICAL',
              'DET_CODE': 'PZWAV',
              'MIN_Z': z['min'],
              'MAX_Z': z['max'],
              'SNR_THR': 3.0,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max'], 
              'OMEGA_MAT': .25,
              'OMEGA_VAC': .75,
              'HUBBLE_PAR': 73,
              'W_EQ_STATE': -1,
              'N_EFF': 3.04,
              'TEMP_CMB': 0,
              'DZ': 0.06,
              'ZSTEP': 2e5,
              'KRN_SCL2': 300,
              'KRN_SCL1': 1200,
              'PIX_DEG': 300,
              'DR_LIM': 1000,
              'DZ_LIM': 0.12,
              'FROM_DENSITY_MAP': False} 
    return header

def gen_detcl_output(ra, dec, z):
    col_id = np.array(range(row_numbers))
    col_ra = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    col_dec = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    col_z = generate_vector(row_numbers, 'float', z['min'], z['max'])
    col_z_err = generate_vector(row_numbers, 'float', 0, 1)
    col_snr = generate_vector(row_numbers, 'float', 3.0, 80)
    col_snr_unique = generate_vector(row_numbers, 'float', 3.0, 80)
    col_rad = generate_vector(row_numbers, 'float', 0.5, 60)
    col_richness = generate_vector(row_numbers, 'float', 0, 1)
    col_lambda_star = generate_vector(row_numbers, 'float', 0, 1)
    col_edge = generate_vector(row_numbers, 'int', 0, 1)
    col_fraction_masked = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'RIGHT_ASCENSION_CLUSTER': pd.Series(col_ra, dtype=np.dtype('f8')),
              'DECLINATION_CLUSTER': pd.Series(col_dec, dtype=np.dtype('f8')),
              'Z_CLUSTER': pd.Series(col_z, dtype=np.dtype('f4')),
              'Z_ERR_CLUSTER': pd.Series(col_z_err, dtype=np.dtype('f4')),
              'SNR_CLUSTER': pd.Series(col_snr, dtype=np.dtype('f4')),
              'SNR_UNIQUE_CLUSTER': pd.Series(col_snr_unique, dtype=np.dtype('f4')),
              'RADIUS_CLUSTER': pd.Series(col_rad, dtype=np.dtype('f4')),
              'RICHNESS_CLUSTER': pd.Series(col_richness, dtype=np.dtype('f4')),
              'LAMBDA_STAR_CLUSTER': pd.Series(col_lambda_star, dtype=np.dtype('f4')),
              'FLAG_EDGE_CLUSTER': pd.Series(col_edge, dtype=np.dtype('f4')),
              'FRAC_MASKED_CLUSTER': pd.Series(col_fraction_masked, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def clean_old_files(dirty_file):
    if os.path.exists(dirty_file): 
        os.remove(dirty_file)


if __name__ == '__main__':
    RA = {'min': 0, 'max': 5}
    DEC = {'min': -2.5, 'max':2.5}
    Z = {'min': 0.1, 'max': 3} 

    amico_file = 'amico_stub.fits'
    pzwav_file = 'pzwav_stub.fits'

    clean_old_files(amico_file)
    clean_old_files(pzwav_file)

    row_numbers = 10
    data_amico = gen_detcl_output(RA, DEC, Z)
    header_amico = gen_amico_header(RA, DEC, Z)
    data_pzwav = gen_detcl_output(RA, DEC, Z)
    header_pzwav = gen_pzwav_header(RA, DEC, Z)

    fitsio.write(amico_file, None, header=header_amico)
    fitsio.write(pzwav_file, None, header=header_pzwav)
    fitsio.write(amico_file, data_amico)
    fitsio.write(pzwav_file, data_pzwav)
