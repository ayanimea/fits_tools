import fitsio
import numpy as np
import pandas as pd
import os

def read(input_folder, file_name):
    data_file = os.path.join(input_folder, file_name)
    data, header = fitsio.read(data_file, header=True)

    data = data.byteswap().newbyteorder('=')
    
    return pd.DataFrame.from_records(data), header

def merge_headers(base_header, in_header):
    in_dict = in_header.records()

    for record in in_dict:
        base_header.add_record(record)

    return base_header 

def characterize_clusters(input_folder, cat_file, det_code, characterization_files):
    
    cat_merge, header_merge = read(input_folder, cat_file)
   
    cat_merge['DET_CODE_NB'] = np.ones(cat_merge.shape[0]) * det_code
    for catalog_file in characterization_files:
        catalog, header = read(input_folder, catalog_file)
        cat_merge = pd.merge(cat_merge, catalog, how='left', on='ID_CLUSTER')
        header_merge = merge_headers(header_merge, header)

    return cat_merge, header_merge

def cat_fully_characterized_clusters(catalogs, header, output_cat_file):
    
    cat_concat = None

    for catalog in catalogs:
        if cat_concat is None:
            cat_concat = catalog
        else:
            cat_concat = pd.concat((cat_concat, catalog))

    cat_concat.rename(columns={'ID_CLUSTER':'ID_DET_CLUSTER',
                               'RICHNESS_VEC':'RICHNESS_VEC_PMEM',
                               'RICHNESS_ERR_VEC': 'RICHNESS_ERR_VEC_PMEM',
                               'RADIUS_VEC':'RADIUS_VEC_PMEM',
                               'RICHNESS':'RICHNESS_PMEM',
                               'RICHNESS_ERR':'RICHNESS_ERR_PMEM',
                               'RADIUS': 'RADIUS_PMEM',
                               'BKG_FRACTION': 'BKG_FRACTION_PMEM'}, inplace=True)

    cat_concat['ID_UNIQUE_CLUSTER'] = np.array(range(cat_concat.shape[0]))
    cat_concat['CROSS_ID_CLUSTER'] = np.ones(cat_concat.shape[0]) * -1
    import pdb; pdb.set_trace()
    fitsio.write(output_cat_file, cat_concat.to_records(index=False), header=header)
    

def clean_keywords(header):
    header.delete('DET_CODE')
    header.delete('DETCODE')
    hubble_const = header['HUBBLE_PAR'] 
    header['HUBBLE_CONST'] = hubble_const
    snr_threshold = header['SNR_THR']
    header['SN_THR'] = snr_threshold
    header.delete('MODEL_ID')
    header.delete('HUBBLE_PAR')
    header.delete('COMMENT')

    return header

if __name__ == '__main__':
    input_folder = os.path.join(os.getcwd(), 'det_rich_output')
    output_folder = os.path.join(os.getcwd(), 'cat_output')
    cat_file = os.path.join(output_folder, 'cat_output.fits')
    test_file = os.path.join(output_folder, 'test.fits')

    if os.path.exists(cat_file):
        os.remove(cat_file)

    if os.path.exists(test_file):
        os.remove(test_file)

    full_amico, header_amico = characterize_clusters(input_folder, 'amico_stub.fits', 1, ('richcl_stub.fits', 'zcl_stub.fits',
                                                    'prof_stub.fits', 'rich_amico_stub.fits'))
    full_pzwav, header_pzwav = characterize_clusters(input_folder, 'pzwav_stub.fits', 2, ('richcl_stub.fits', 'zcl_stub.fits',
                                                    'prof_stub.fits', 'rich_amico_stub.fits'))
    header_amico['DET_CODE_1'] = 'AMICO'
    header_pzwav['DET_CODE_2'] = 'PZWAV'
    header = merge_headers(header_amico, header_pzwav)

    header = clean_keywords(header)
    cat_fully_characterized_clusters((full_amico, full_pzwav), header, cat_file)
