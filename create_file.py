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

def gen_zcl_header():
    return None

def gen_prof_header(ra, dec, z):
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

def gen_rich_amico_header():
    header = {'COORDSYS': 'SPHERICAL',
              'MAX_DEC': 'SPHERICAL', 
              'DETCODE': 'AMICO',
              'MODEL_ID': 0,
              'SNR_THR': 3.0,
              'MAX_NB': 5,
              'MIN_PROB': .75,
              'MEMB_CODE': 'AMICO'}

    return header


def gen_richcl_header(ra, dec):
    header = {'DETCODE': 'PZWAV',
              'MODEL_ID': '',
              'SNR_THR': 3.0,
              'MAX_NB': 5,
              'MIN_PROB': .75,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max']} 
    return header

def gen_zcl_output(z):
    col_id = np.array(range(row_numbers))
    col_z = generate_vector(row_numbers, 'float', z['min'], z['max'])
    col_z_err = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'Z_ZCL': pd.Series(col_z, dtype=np.dtype('f4')),
              'Z_ZCL_ERR': pd.Series(col_z_err, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_prof_output(ra, dec):
    col_id = np.array(range(row_numbers))
    col_ra_cen_bestfit = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    col_dec_cen_bestfit = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    col_log_scale_radius_bestfit = generate_vector(row_numbers, 'float', 0, 40)
    col_ellipticity_bestfit = generate_vector(row_numbers, 'float', 0.5, 3)
    col_pa_bestfit = generate_vector(row_numbers, 'float', 0, 1)
    col_log_background_bestfit = generate_vector(row_numbers, 'float', 0, 1)
    col_nofa_bestfit = generate_vector(row_numbers, 'float', 0, 1)
    col_minus_log_likelihood = generate_vector(row_numbers, 'float', 0, 1)
    col_deblending_order = generate_vector(row_numbers, 'float', 0, 1)
    col_bic = generate_vector(row_numbers, 'float', 0, 1)
    col_fit_nfev = generate_vector(row_numbers, 'float', 0, 1)
    col_ra_cen_guess = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    col_dec_cen_guess = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    col_log_scale_radius_guess = generate_vector(row_numbers, 'float', 0, 1)
    col_elliptcity_guess = generate_vector(row_numbers, 'float', 0, 1)
    col_pa_guess = generate_vector(row_numbers, 'float', 0, 1)
    col_log_background_guess = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'RA_CEN_BESTFIT': pd.Series(col_ra_cen_bestfit, dtype=np.dtype('f4')),
              'DEC_CEN_BESTFIT': pd.Series(col_dec_cen_bestfit, dtype=np.dtype('f4')),
              'LOG_SCALE_RADIUS_BESTFIT': pd.Series(col_log_scale_radius_bestfit, dtype=np.dtype('f4')),
              'ELLIPTICITY_BESTFIT': pd.Series(col_ellipticity_bestfit, dtype=np.dtype('f4')),
              'PA_BESTFIT': pd.Series(col_pa_bestfit, dtype=np.dtype('f4')),
              'LOG_BACKGROUND_BESTFIT': pd.Series(col_log_background_bestfit, dtype=np.dtype('f4')),
              'NOFA_BESTFIT': pd.Series(col_nofa_bestfit, dtype=np.dtype('f4')),
              'MINUS_LOG_LIKELIHOOD': pd.Series(col_minus_log_likelihood, dtype=np.dtype('f4')),
              'DEBLENDING_ORDER': pd.Series(col_deblending_order, dtype=np.dtype('f4')),
              'BIC': pd.Series(col_bic, dtype=np.dtype('f4')),
              'FIT_NFEV': pd.Series(col_fit_nfev, dtype=np.dtype('f4')),
              'RA_CEN_GUESS': pd.Series(col_ra_cen_guess, dtype=np.dtype('f4')),
              'DEC_CEN_GUESS': pd.Series(col_dec_cen_guess, dtype=np.dtype('f4')),
              'LOG_SCALE_RADIUS_GUESS': pd.Series(col_log_scale_radius_guess, dtype=np.dtype('f4')),
              'ELLIPTICITY_GUESS': pd.Series(col_elliptcity_guess, dtype=np.dtype('f4')),
              'PA_GUESS': pd.Series(col_pa_guess, dtype=np.dtype('f4')),
              'LOG_BACKGROUND_GUESS': pd.Series(col_log_background_guess, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_rich_amico_output():
    col_obj_id = generate_vector(row_numbers, 'int', 1, 10000)
    col_id = np.array(range(row_numbers))
    col_pmem = generate_vector(row_numbers, 'float', 0, 1)
    col_pmem_err = generate_vector(row_numbers, 'float', 0, 1)
    col_pmem_rad = generate_vector(row_numbers, 'float', 0, 40)
    col_pmem_z = generate_vector(row_numbers, 'float', 0.5, 3)
    col_pmem_rs = generate_vector(row_numbers, 'float', 0, 1)
    col_pmem_rs_err = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'OBJECT_ID': pd.Series(col_obj_id, dtype=np.dtype('i8')),
              'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'PMEM': pd.Series(col_pmem, dtype=np.dtype('f4')),
              'PMEM_ERR': pd.Series(col_pmem_err, dtype=np.dtype('f4')),
              'PMEM_RAD': pd.Series(col_pmem_rad, dtype=np.dtype('f4')),
              'PMEM_Z': pd.Series(col_pmem_z, dtype=np.dtype('f4')),
              'PMEM_RS': pd.Series(col_pmem_rs, dtype=np.dtype('f4')),
              'PMEM_RS_ERR': pd.Series(col_pmem_rs_err, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_richcl_output():
    col_id = np.array(range(row_numbers))
    col_rich_vec = generate_vector(row_numbers, 'float', 1, 3000)
    col_rich_err_vec = generate_vector(row_numbers, 'float', 1, 80)
    col_rad_vec = generate_vector(row_numbers, 'float', 1, 80)
    col_rich = generate_vector(row_numbers, 'float', 1, 3000)
    col_rich_err = generate_vector(row_numbers, 'float', 1, 80)
    col_rad = generate_vector(row_numbers, 'float', 3.0, 80)
    col_bkg_frac = generate_vector(row_numbers, 'float', 0, 1)
    col_rich_vec_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rich_err_vec_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rad_vec_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rich_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rich_err_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rad_rs = generate_vector(row_numbers, 'float', 0, 10)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'RICHNESS_VEC': pd.Series(col_rich_vec, dtype=np.dtype('f4')),
              'RICHNESS_ERR_VEC': pd.Series(col_rich_err_vec, dtype=np.dtype('f4')),
              'RADIUS_VEC': pd.Series(col_rad_vec, dtype=np.dtype('f4')),
              'RICHNESS': pd.Series(col_rich, dtype=np.dtype('f4')),
              'RICHNESS_ERR': pd.Series(col_rich_err, dtype=np.dtype('f4')),
              'RADIUS': pd.Series(col_rad, dtype=np.dtype('f4')),
              'BKG_FRACTION': pd.Series(col_bkg_frac, dtype=np.dtype('f4')),
              'RICHNESS_VEC_RS': pd.Series(col_rich_vec_rs, dtype=np.dtype('f4')),
              'RICHNESS_ERR_VEC_RS': pd.Series(col_rich_err_vec_rs, dtype=np.dtype('f4')),
              'RADIUS_VEC_RS': pd.Series(col_rad_vec_rs, dtype=np.dtype('f4')),
              'RICHNESS_RS': pd.Series(col_rich_rs, dtype=np.dtype('f4')),
              'RICHNESS_ERR_RS': pd.Series(col_rich_err_rs, dtype=np.dtype('f4')),
              'RADIUS_RS': pd.Series(col_rad_rs, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

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
    # Constants
    RA = {'min': 0, 'max': 5}
    DEC = {'min': -2.5, 'max':2.5}
    Z = {'min': 0.1, 'max': 3} 
    row_numbers = 2 
    output_folder = os.path.join(os.getcwd(), 'det_rich_output')

    # Choose paths
    amico_file = os.path.join(output_folder, 'amico_stub.fits')
    pzwav_file = os.path.join(output_folder, 'pzwav_stub.fits')
    richcl_file = os.path.join(output_folder, 'richcl_stub.fits')
    rich_amico_file = os.path.join(output_folder, 'rich_amico_stub.fits')
    zcl_file = os.path.join(output_folder, 'zcl_stub.fits')
    prof_file = os.path.join(output_folder, 'prof_stub.fits')

    # Clean old files
    clean_old_files(amico_file)
    clean_old_files(pzwav_file)
    clean_old_files(richcl_file)
    clean_old_files(rich_amico_file)
    clean_old_files(zcl_file)
    clean_old_files(prof_file)


    # Generate headers
    header_amico = gen_amico_header(RA, DEC, Z)
    header_pzwav = gen_pzwav_header(RA, DEC, Z)
    header_richcl = gen_richcl_header(RA, DEC)
    header_rich_amico = gen_rich_amico_header()
    header_zcl = gen_zcl_header()
    header_prof = gen_prof_header(RA, DEC, Z)
    
    # Generate data 
    data_amico = gen_detcl_output(RA, DEC, Z)
    data_pzwav = gen_detcl_output(RA, DEC, Z)
    data_richcl = gen_richcl_output()
    data_rich_amico = gen_rich_amico_output()
    data_zcl = gen_zcl_output(Z)
    data_prof = gen_prof_output(RA, DEC)

    # Write primary HDU
    fitsio.write(amico_file, None, header=header_amico)
    fitsio.write(pzwav_file, None, header=header_pzwav)
    fitsio.write(richcl_file, None, header=header_richcl)
    fitsio.write(rich_amico_file, None, header=header_rich_amico)
    fitsio.write(zcl_file, None, header=header_zcl)
    fitsio.write(prof_file, None, header=header_prof)

    # Write catalogs
    fitsio.write(amico_file, data_amico)
    fitsio.write(pzwav_file, data_pzwav)
    fitsio.write(richcl_file, data_richcl)
    fitsio.write(rich_amico_file, data_rich_amico)
    fitsio.write(zcl_file, data_zcl)
    fitsio.write(prof_file, data_prof)
