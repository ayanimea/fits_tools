import fitsio
import numpy as np

def select_data(data_file):

    nrows = -1

    #with fitsio.FITS(data_file, 'r') as fits:
    #    data = fits[1][:]
    #    nrows = fits[1].get_nrows()

    data = None 
    fits = fitsio.FITS(data_file) 

    import pdb; pdb.set_trace()
    return data, nrows


if __name__ == "__main__":
    
    data, nrows = select_data("/home/user/Work/Projects/ial_workspace/pzwav/data/new_pdf_mock2_subsample_16.4deg2.fits")
    

    print(f"nrows: {nrows}\nnp.mean: {np.mean(data['euc_err_vis'])}")
