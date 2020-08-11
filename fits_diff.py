import fitsio
import sys
import numpy as np

def col_compare(col1, col2, name):
    result = np.equal(col1, col2)
    print(f"columns {name} are equals: {result}")

    return result

def compare__out_files(file1, file2):
    content_file1 = fitsio.read(file1)
    content_file2 = fitsio.read(file2)
    
    result = col_compare(content_file1['ID'], content_file2['CLUSTER_ID'], "ID / CLUSTER_ID")
    result = result and col_compare(content_file1['RA'], content_file2['RA'], "RA / RA")
    result = result and col_compare(content_file1['DEC'], content_file2['DEC'], "DEC / DEC")
    result = result and col_compare(content_file1['z'], content_file2['Z'], "z / Z")
    result = result and col_compare(content_file1['z_err'], content_file2['Z_ERR'], "z_err / Z_ERR")
    result = result and col_compare(content_file1['SNR'], content_file2['SNR'], "SNR / SNR")
    result = result and col_compare(content_file1['richness'], content_file2['RICHNESS'], "richness / RICHNESS")
    result = result and col_compare(content_file1['radius'], content_file2['RADIUS'], "radius / RADIUS")
    result = result and col_compare(content_file1['mask_edge'], content_file2['MASK_EDGE'], "mask_edge / MASK_EDGE")

    return result
    
def compare_gal_files(file1, file2):
    content_file1 = fitsio.read(file1)
    content_file2 = fitsio.read(file2)
    
    result = np.equal(content_file1, content_file2)

    return result

if __name__ == "__main__":
    # file1 is old
    # file2 is new
    
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    print(file1)
    print(file2)

    if sys.argv[1] is "out":
        print(f"Result: {compare_out_files(file1, file2)}")
    else:
        print(f"Result: {compare_gal_files(file1, file2)}")
