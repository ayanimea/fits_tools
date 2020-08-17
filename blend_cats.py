import fitsio
import numpy as np
import pandas as pd
import os

def read(input_folder, file_name):
    data_file = os.path.join(input_folder, file_name)
    data = fitsio.read(data_file)

    data = data.byteswap().newbyteorder('=')
    
    return pd.DataFrame.from_records(data)


if __name__ == '__main__':
    input_folder = os.path.join(os.getcwd(), 'det_rich_output')
    output_folder = os.path.join(os.getcwd(), 'cat_output')
    cat_file = os.path.join(output_folder, 'cat_output.fits')
    os.remove(cat_file)

    amico = read(input_folder, 'amico_stub.fits')
    pzwav = read(input_folder, 'pzwav_stub.fits')
    richcl = read(input_folder, 'richcl_stub.fits')
    rich = read(input_folder, 'rich_amico_stub.fits')

    full_pzwav = pd.merge(pzwav, richcl, how='left', on='ID_CLUSTER')
    full_amico = pd.merge(amico, rich, how='left', on='ID_CLUSTER')
    full_det = pd.concat((amico, rich))

    cat = full_det

    fitsio.write(cat_file, cat.to_records())
