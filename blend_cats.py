import fitsio
from fitsio import FITSHDR
import numpy as np
from astropy.table import Table, join, vstack
import os

def read(input_folder, file_name):
    data_file = os.path.join(input_folder, file_name)
    data, header = fitsio.read(data_file, header=True)

    data = data.byteswap().newbyteorder('=')
    return Table(data), header

def merge_headers(base_header, in_header):
    keywords_list = in_header.records()
    base_header_list = base_header.records()
    to_delete_keywords = ['TFORM', 'FROM_DENSITY_MAP',
                          'TTYPE', 'NAXIS', 'TFIELDS', 'GCOUNT', 'PCOUNT',
                          'BITPIX', 'XTENSION'] 

    out_dict = [] 
    for key in base_header_list:
        if not any(keyword in key['name'] for keyword in to_delete_keywords):
            out_dict.append(key) 

    for key in keywords_list:
        if not any(keyword in key['name'] for keyword in to_delete_keywords):
            out_dict.append(key)

    base_header = FITSHDR(out_dict)

    return base_header 

def characterize_clusters(input_folder, cat_file, det_code, characterization_files):
    
    cat_merge, header_merge = read(input_folder, cat_file)
   
    cat_merge['DET_CODE_NB'] = np.ones(len(cat_merge)) * det_code
    for catalog_file in characterization_files:
        catalog, header = read(input_folder, catalog_file)
        cat_merge = join(cat_merge, catalog, keys='ID_CLUSTER')
        header_merge = merge_headers(header_merge, header)

    return cat_merge, header_merge

def cat_fully_characterized_clusters(catalogs, header, output_cat_file):
    
    cat_concat = None

    for catalog in catalogs:
        if cat_concat is None:
            cat_concat = catalog
        else:
            cat_concat = vstack((cat_concat, catalog))
    cat_concat.rename_columns(['ID_CLUSTER', 'RICHNESS_VEC', 'RICHNESS_ERR_VEC',
                               'RADIUS_VEC', 'RICHNESS', 'RICHNESS_ERR', 'RADIUS',
                               'BKG_FRACTION'],
                              ['ID_DET_CLUSTER', 'RICHNESS_VEC_PMEM', 'RICHNESS_ERR_VEC_PMEM',
                               'RADIUS_VEC_PMEM', 'RICHNESS_PMEM', 'RICHNESS_ERR_PMEM', 'RADIUS_PMEM',
                               'BKG_FRACTION_PMEM'])

    cat_concat['ID_UNIQUE_CLUSTER'] = np.array(range(len(cat_concat)))
    cat_concat['CROSS_ID_CLUSTER'] = np.ones(len(cat_concat)) * -1
    fitsio.write(output_cat_file, cat_concat.as_array(), header=header)
    

def clean_keywords(header):
    header.delete('DET_CODE')
    header.delete('DETCODE')
    header.delete('MODEL_ID')
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
