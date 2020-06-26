from astropy.io import fits

if __name__ == '__main__':
    header = fits.getheader("Work/Projects/ial_workspace/pzwav/input/paramsPZdefault.fits")
    header['SN_THR'] = 4.7
    fits.writeto('Work/Projects/ial_workspace/pzwav/input/params_pz_thresh_47.fits', None, header)
