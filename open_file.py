import fitsio
import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
import traceback

data_files = 'pdf_mock1_*.fits'

input_filepath = glob.glob(data_files)
print(f'Input filepath: {input_filepath}')

print("******************** ASTROPY *******************")

for one_file in input_filepath:
    with fits.open(one_file, mode="update", memmap=False) as hdu:
        print(f'======= {one_file}')
        try:
            t = Table.read(hdu[1])
            print(f'Mean: {np.mean(np.array(t["PHZ_PDF"].astype(np.float)))}')
        except:
            traceback.print_exc()
        # hdu[1].columns['PDF'].name = 'PHZ_PDF'
        # hdu[1].columns['ID'].name = 'OBJECT_ID'
        # hdu.flush()


print("******************** FITSIO *******************")
for one_file in input_filepath:
    print(f'======= {one_file}')
    try:
        data = fitsio.read(one_file)
        print(f'Data mean: {np.mean(np.array(data["PHZ_PDF"].astype(np.float)))}')
    except:
        traceback.print_exc()
