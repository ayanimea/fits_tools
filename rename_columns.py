import glob
import numpy as np
from astropy.io import fits
import traceback

data_files = 'pdf_mock1_*.fits'

input_filepath = glob.glob(data_files)
print(f'Input filepath: {input_filepath}')

for one_file in input_filepath:
    with fits.open(one_file, mode="update") as hdu:
        print(f'===== {one_file}')
        hdu[1].columns['PDF'].name = 'PHZ_PDF'
        hdu[1].columns['ID'].name = 'OBJECT_ID'
        hdu.flush()
