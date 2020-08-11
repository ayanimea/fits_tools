import fitsio
import numpy as np
import os

def generate_vector(length, dtype):
    new_vector = np.random.random(length).astype(dtype)
    return new_vector

def gen_amico_header():
    header = None
    return header

def gen_pzwav_header():
    header = None
    return header

def gen_detcl_output():
    col_id = range(row_numbers)
    col_ra = generate_vector(row_numbers, dtype=np.float64)
    col_dec = generate_vector(row_numbers, dtype=np.float64)
    col_z = generate_vector(row_numbers, dtype=np.float32)
    col_z_err = generate_vector(row_numbers, dtype=np.float32)
    col_snr = generate_vector(row_numbers, dtype=np.float32)
    col_snr_unique = generate_vector(row_numbers, dtype=np.float32)
    col_rad = generate_vector(row_numbers, dtype=np.float32)
    col_richness = generate_vector(row_numbers, dtype=np.float32)
    col_lambda_star = generate_vector(row_numbers, dtype=np.float32)
    col_edge = generate_vector(row_numbers, dtype=np.float32)
    col_fraction_masked = generate_vector(row_numbers, dtype=np.float32)
    
    matrix = [col_id, col_ra,
                  col_dec, col_z,
                  col_z_err, col_snr,
                  col_snr_unique, col_rad,
                  col_richness, col_lambda_star,
                  col_edge, col_fraction_masked]


    names=[('ID_CLUSTER', '>i8'), ('RIGHT_ASCENSION_CLUSTER', '>f8'),
           ('DECLINATION_CLUSTER', '>f8'), ('Z_CLUSTER', '>f4'),
           ('Z_ERR_CLUSTER', '>f4'), ('SNR_CLUSTER', '>f4'),
           ('SNR_UNIQUE_CLUSTER', '>f4'), ('RADIUS_CLUSTER', '>f4'),
           ('RICHNESS_CLUSTER', '>f4'), ('LAMBDA_STAR_CLUSTER', '>f4'),
          ('FLAG_EDGE_CLUSTER', '>f4'), ('FRAC_MASKED_CLUSTER', '>f4')]

    data = np.zeros(10, dtype=names) 

    return data

def clean_old_files(dirty_file):
    if os.path.exists(dirty_file): 
        os.remove(dirty_file)


if __name__ == '__main__':
    amico_file = 'amico_stub.fits'
    pzwav_file = 'pzwav_stub.fits'

    clean_old_files(amico_file)
    clean_old_files(pzwav_file)

    row_numbers = 10
    data_amico = gen_detcl_output()
    header_amico = gen_amico_header()
    data_pzwav = gen_detcl_output()
    header_pzwav = gen_pzwav_header()

    fitsio.write(amico_file, data_amico, header=header_amico)
    fitsio.write(pzwav_file, data_pzwav, header=header_pzwav)
