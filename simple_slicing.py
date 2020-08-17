import fitsio
import numpy as np

def delete_where(gal, pdf, filters):

    # Criteria is a dictionary with col name and val limit

    gal = np.delete(gal, filters)
    pdf = np.delete(pdf, filters)

    return gal, pdf

def slice_gal(gal_in, gal_out, pdf_in, pdf_out, criteria_min, criteria_max):

    # Criteria is a dictionary with col name and val limit

    gal = fitsio.read(gal_in)
    pdf = fitsio.read(pdf_in)
    filter_min_ra = np.where(gal['ra_gal'] < criteria_min['ra_gal'])
    filter_max_ra = np.where(gal['ra_gal'] > criteria_max['ra_gal'])
    filter_min_dec = np.where(gal['dec_gal'] < criteria_min['dec_gal'])
    filter_max_dec = np.where(gal['dec_gal'] > criteria_max['dec_gal'])

    filters = np.concatenate((filter_min_ra, filter_max_ra, filter_min_dec, filter_max_dec), axis=None)
    filters = np.unique(filters)
    gal, pdf = delete_where(gal, pdf, filters)

    fitsio.write(gal_out, gal)
    fitsio.write(pdf_out, pdf)

def slices_mass_redshift(matching_in, matching_out, criteria_min):
    matching = fitsio.read(matching_in)

    filter_min_mass = np.where(matching['H_MASS'] < criteria_min['H_MASS'])
    filter_min_redshift = np.where(matching['C_Z'] < criteria_min['C_Z'])
    filter_min_match = np.where(matching['MATCH'] == criteria_min['MATCH'])
    filters = np.concatenate((filter_min_mass, filter_min_redshift, filter_min_match), axis=None)
    matching = np.delete(matching, filters)

    fitsio.write(matching_out, matching)

if __name__ == "__main__":
    criteria_min = {'ra_gal':13.4, 'dec_gal':72.55}
    criteria_max = {'ra_gal':13.8, 'dec_gal':72.65}
    pdf_in = "/home/user/Work/Projects/ial_workspace/pzwav/data/new_pdf_mock2_subsample_34.16deg2.fits"
    gal_in = "/home/user/Work/Projects/ial_workspace/pzwav/data/mock2_subsample_34.16deg2.fits"
    pdf_out = "/home/user/Work/Projects/tools/sliced_new_pdf_mock2_subsample_34.16deg2.fits"
    gal_out = "/home/user/Work/Projects/tools/sliced_mock2_subsample_34.16deg2.fits"
    slice_gal(gal_in, gal_out, pdf_in, pdf_out, criteria_min, criteria_max)

    # matching_in = "/home/user/Work/Projects/OU_DET_CL_PZWAV/DET_CL_PZWav/tests/manual_test/output_dir/match-current/agob_mock2_matching_single_H_CFC4_mock2_.fits"
    # matching_out = "/home/user/Work/Projects/tools/slice_matching"
    # criteria_min = {'H_MASS':14, 'C_Z':1.2 , 'MATCH':'T'}
    # slices_mass_redshift(matching_in, matching_out, criteria_min)
