from astropy.io import fits

def open_and_print(filename):
    print(f'==== File: {filename}')
    hdul = fits.open(filename)
    data = hdul[1].data
    print(data.shape)
    print(data.dtype.name)

if __name__ == '__main__':
    filename = '/home/user/Work/Projects/ial_workspace/pzwav/data/subsamples_mock1/subsample_25_Durham_Photreal_300deg2_blind_SC8.fits' 
    open_and_print(filename)
    filename = '/media/sf_Euclid/Dataset/subsamples_mock1_martin_CFC4/pdf_mock1_25deg2.fits' 
    open_and_print(filename)
    filename = '/home/user/Work/Projects/ial_workspace/pzwav/data/subsamples_mock1_martin/pdf_mock1_25deg2.fits' 
    open_and_print(filename)
