from astropy.io import fits
import os
import numpy as np

# OU:
dir_ou = "/home/user/Work/Projects/ial_workspace/mock1_25sqdeg_proto"
dir_pf = "/home/user/Work/Projects/ial_workspace/pzwav/detections/output"

fils_ou=['CFC4M2A24.99H30SN2.5V2.1_0.06.density.fits',
        'CFC4M2A24.99H30SN2.5V2.1_0.06.mask.fits',
        'CFC4M2A24.99H30SN2.5V2.1_0.06.wavelet.fits',
        'CFC4M2A24.99H30SN2.5V2.1.blank_0.06.density.fits',
        'CFC4M2A24.99H30SN2.5V2.1.blank_0.06.mask.fits',
        'CFC4M2A24.99H30SN2.5V2.1.blank_0.06.wavelet.fits']

fils_pf=['mock1_25sq_inter_galaxies.fits',
        'mock1_25sq_inter_masks.fits',
        'mock1_25sq_inter_density.fits',
        'mock1_25sq_inter_blank_galaxies.fits',
        'mock1_25sq_inter_masks.fits',
        'mock1_25sq_inter_blank_density.fits']

def load_hdu_data(f, header=False):
    return f[header].data

def header_list(file_in):
    return fits.open(file_in)

def stat_im(im):
    return np.mean(im), np.std(im)

def main(dir1, fil1, dir2, fil2):
    print("#####")

    filepath1 = os.path.join(dir1, fil1)
    filepath2 = os.path.join(dir2, fil2)
    hdu_list1 = header_list(filepath1)
    hdu_list2 = header_list(filepath2)

    index = 0

    if len(hdu_list1) != len(hdu_list2):
        print('WARNING: Both files have different number of HDU')

    max_index = min(len(hdu_list1), len(hdu_list2))

    for index in range(0, max_index):
        print(f'***HDU : {index}')
        d1 = load_hdu_data(hdu_list1, header=index)
        d2 = load_hdu_data(hdu_list2, header=index)

        print(f' Mean1: {stat_im(d1)[0]:3.2f}\t\t\t | Mean2: {stat_im(d2)[0]:3.2f}')
        print(f' StdDev11: {stat_im(d1)[1]:3.2f}\t\t\t | StdDev2: {stat_im(d2)[1]:3.2f}')
        index += 1

if __name__=="__main__":
    for index in range(0, len(fils_ou)):
        print(f'======== OU =======')
        print(f'=== file: {fils_ou[index]}\t | file: {fils_pf[index]}')
        main(dir_ou, fils_ou[index], dir_pf, fils_pf[index]) 
