import fitsio
import numpy as np
import numpy.lib.recfunctions

def merge_catalogs(gal_in, pdf_in, cat_out):

    gal = fitsio.read(gal_in)
    pdf = fitsio.read(pdf_in)

    unified_gal_pdf = np.lib.recfunctions.join_by('OBJECT_ID', gal, pdf, jointype='inner')

    fitsio.write(cat_out, unified_gal_pdf)


if __name__ == "__main__":
    gal_in = "/home/user/Work/Projects/ial_workspace/pzwav/data/mock2_subsample_8.55deg2_SC8.fits"
    pdf_in = "/home/user/Work/Projects/ial_workspace/pzwav/data/new_pdf_mock2_subsample_8.55deg2_SC8.fits"
    cat_out = "/home/user/Work/Projects/tools/unified_mock2_subsample_8.55deg2_SC8.fits"
    merge_catalogs(gal_in, pdf_in, cat_out)
