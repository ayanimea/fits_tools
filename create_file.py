import fitsio
import numpy as np
import os
import pandas as pd

def generate_vector(length, num_type, mini, maxi):

    if num_type is 'float':
        new_vector = np.random.rand(length) * (maxi - mini) + mini
    elif num_type is 'int':
        new_vector = np.random.random_integers(mini, maxi, length)        

    return new_vector

def gen_zcl_header():
    return None

def gen_prof_header(ra, dec, z):
    header = {'COORDSYS': 'SPHERICAL',
              'DET_CODE': 'AMICO',
              'MIN_Z': z['min'],
              'MAX_Z': z['max'],
              'SNR_THR': 3.0,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max'],
              'OMEGA_MAT': .25,
              'OMEGA_VAC': .75,
              'HUBBLE_PAR': 73,
              'W_EQ_STATE': -1,
              'N_EFF': 3.04,
              'TEMP_CMB': 0, 
              'CUBE_XY_STEP': 5,
              'MAX_AREA_DEG': 40,
              'L_BORDER_DEG': 0.1} 
    return header

def gen_amico_header(ra, dec, z):
    header = {'COORDSYS': 'SPHERICAL',
              'DET_CODE': 'AMICO',
              'MIN_Z': z['min'],
              'MAX_Z': z['max'],
              'SNR_THR': 3.0,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max'],
              'OMEGA_MAT': .25,
              'OMEGA_VAC': .75,
              'HUBBLE_PAR': 73,
              'W_EQ_STATE': -1,
              'N_EFF': 3.04,
              'TEMP_CMB': 0, 
              'CUBE_XY_STEP': 5,
              'MAX_AREA_DEG': 40,
              'L_BORDER_DEG': 0.1} 
    return header

def gen_pzwav_header(ra, dec, z):
    header = {'COORDSYS': 'SPHERICAL',
              'DET_CODE': 'PZWAV',
              'MIN_Z': z['min'],
              'MAX_Z': z['max'],
              'SNR_THR': 3.0,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max'], 
              'OMEGA_MAT': .25,
              'OMEGA_VAC': .75,
              'HUBBLE_PAR': 73,
              'W_EQ_STATE': -1,
              'N_EFF': 3.04,
              'TEMP_CMB': 0,
              'DZ': 0.06,
              'ZSTEP': 2e5,
              'KRN_SCL2': 300,
              'KRN_SCL1': 1200,
              'PIX_DEG': 300,
              'DR_LIM': 1000,
              'DZ_LIM': 0.12,
              'FROM_DENSITY_MAP': False} 
    return header

def gen_rich_amico_header():
    header = {'COORDSYS': 'SPHERICAL',
              'MAX_DEC': 'SPHERICAL', 
              'DETCODE': 'AMICO',
              'MODEL_ID': 0,
              'SNR_THR': 3.0,
              'MAX_NB': 5,
              'MIN_PROB': .75,
              'MEMB_CODE': 'AMICO'}

    return header


def gen_richcl_header(ra, dec):
    header = {'DETCODE': 'PZWAV',
              'MODEL_ID': '',
              'SNR_THR': 3.0,
              'MAX_NB': 5,
              'MIN_PROB': .75,
              'MIN_RA': ra['min'],
              'MAX_RA': ra['max'],
              'MIN_DEC': dec['min'],
              'MAX_DEC': dec['max']} 
    return header

def gen_zcl_output(z):
    col_id = np.array(range(row_numbers))
    col_z = generate_vector(row_numbers, 'float', z['min'], z['max'])
    col_z_err = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'Z_ZCL': pd.Series(col_z, dtype=np.dtype('f4')),
              'Z_ZCL_ERR': pd.Series(col_z_err, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_prof_output(ra, dec):
    col_id = np.array(range(row_numbers))
    col_ra_cen_bestfit = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    col_dec_cen_bestfit = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    col_log_scale_radius_bestfit = generate_vector(row_numbers, 'float', 0, 40)
    col_ellipticity_bestfit = generate_vector(row_numbers, 'float', 0.5, 3)
    col_pa_bestfit = generate_vector(row_numbers, 'float', 0, 1)
    col_log_background_bestfit = generate_vector(row_numbers, 'float', 0, 1)
    col_nofa_bestfit = generate_vector(row_numbers, 'float', 0, 1)
    col_minus_log_likelihood = generate_vector(row_numbers, 'float', 0, 1)
    col_deblending_order = generate_vector(row_numbers, 'float', 0, 1)
    col_bic = generate_vector(row_numbers, 'float', 0, 1)
    col_fit_nfev = generate_vector(row_numbers, 'float', 0, 1)
    col_ra_cen_guess = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    col_dec_cen_guess = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    col_log_scale_radius_guess = generate_vector(row_numbers, 'float', 0, 1)
    col_elliptcity_guess = generate_vector(row_numbers, 'float', 0, 1)
    col_pa_guess = generate_vector(row_numbers, 'float', 0, 1)
    col_log_background_guess = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'RA_CEN_BESTFIT': pd.Series(col_ra_cen_bestfit, dtype=np.dtype('f4')),
              'DEC_CEN_BESTFIT': pd.Series(col_dec_cen_bestfit, dtype=np.dtype('f4')),
              'LOG_SCALE_RADIUS_BESTFIT': pd.Series(col_log_scale_radius_bestfit, dtype=np.dtype('f4')),
              'ELLIPTICITY_BESTFIT': pd.Series(col_ellipticity_bestfit, dtype=np.dtype('f4')),
              'PA_BESTFIT': pd.Series(col_pa_bestfit, dtype=np.dtype('f4')),
              'LOG_BACKGROUND_BESTFIT': pd.Series(col_log_background_bestfit, dtype=np.dtype('f4')),
              'NOFA_BESTFIT': pd.Series(col_nofa_bestfit, dtype=np.dtype('f4')),
              'MINUS_LOG_LIKELIHOOD': pd.Series(col_minus_log_likelihood, dtype=np.dtype('f4')),
              'DEBLENDING_ORDER': pd.Series(col_deblending_order, dtype=np.dtype('f4')),
              'BIC': pd.Series(col_bic, dtype=np.dtype('f4')),
              'FIT_NFEV': pd.Series(col_fit_nfev, dtype=np.dtype('f4')),
              'RA_CEN_GUESS': pd.Series(col_ra_cen_guess, dtype=np.dtype('f4')),
              'DEC_CEN_GUESS': pd.Series(col_dec_cen_guess, dtype=np.dtype('f4')),
              'LOG_SCALE_RADIUS_GUESS': pd.Series(col_log_scale_radius_guess, dtype=np.dtype('f4')),
              'ELLIPTICITY_GUESS': pd.Series(col_elliptcity_guess, dtype=np.dtype('f4')),
              'PA_GUESS': pd.Series(col_pa_guess, dtype=np.dtype('f4')),
              'LOG_BACKGROUND_GUESS': pd.Series(col_log_background_guess, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_rich_amico_output():
    col_obj_id = generate_vector(row_numbers, 'int', 1, 10000)
    col_id = np.array(range(row_numbers))
    col_pmem = generate_vector(row_numbers, 'float', 0, 1)
    col_pmem_err = generate_vector(row_numbers, 'float', 0, 1)
    col_pmem_rad = generate_vector(row_numbers, 'float', 0, 40)
    col_pmem_z = generate_vector(row_numbers, 'float', 0.5, 3)
    col_pmem_rs = generate_vector(row_numbers, 'float', 0, 1)
    col_pmem_rs_err = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'OBJECT_ID': pd.Series(col_obj_id, dtype=np.dtype('i8')),
              'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'PMEM': pd.Series(col_pmem, dtype=np.dtype('f4')),
              'PMEM_ERR': pd.Series(col_pmem_err, dtype=np.dtype('f4')),
              'PMEM_RAD': pd.Series(col_pmem_rad, dtype=np.dtype('f4')),
              'PMEM_Z': pd.Series(col_pmem_z, dtype=np.dtype('f4')),
              'PMEM_RS': pd.Series(col_pmem_rs, dtype=np.dtype('f4')),
              'PMEM_RS_ERR': pd.Series(col_pmem_rs_err, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_richcl_output():
    col_id = np.array(range(row_numbers))
    col_rich_vec = generate_vector(row_numbers, 'float', 1, 3000)
    col_rich_err_vec = generate_vector(row_numbers, 'float', 1, 80)
    col_rad_vec = generate_vector(row_numbers, 'float', 1, 80)
    col_rich = generate_vector(row_numbers, 'float', 1, 3000)
    col_rich_err = generate_vector(row_numbers, 'float', 1, 80)
    col_rad = generate_vector(row_numbers, 'float', 3.0, 80)
    col_bkg_frac = generate_vector(row_numbers, 'float', 0, 1)
    col_rich_vec_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rich_err_vec_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rad_vec_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rich_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rich_err_rs = generate_vector(row_numbers, 'float', 0, 10)
    col_rad_rs = generate_vector(row_numbers, 'float', 0, 10)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'RICHNESS_VEC': pd.Series(col_rich_vec, dtype=np.dtype('f4')),
              'RICHNESS_ERR_VEC': pd.Series(col_rich_err_vec, dtype=np.dtype('f4')),
              'RADIUS_VEC': pd.Series(col_rad_vec, dtype=np.dtype('f4')),
              'RICHNESS': pd.Series(col_rich, dtype=np.dtype('f4')),
              'RICHNESS_ERR': pd.Series(col_rich_err, dtype=np.dtype('f4')),
              'RADIUS': pd.Series(col_rad, dtype=np.dtype('f4')),
              'BKG_FRACTION': pd.Series(col_bkg_frac, dtype=np.dtype('f4')),
              'RICHNESS_VEC_RS': pd.Series(col_rich_vec_rs, dtype=np.dtype('f4')),
              'RICHNESS_ERR_VEC_RS': pd.Series(col_rich_err_vec_rs, dtype=np.dtype('f4')),
              'RADIUS_VEC_RS': pd.Series(col_rad_vec_rs, dtype=np.dtype('f4')),
              'RICHNESS_RS': pd.Series(col_rich_rs, dtype=np.dtype('f4')),
              'RICHNESS_ERR_RS': pd.Series(col_rich_err_rs, dtype=np.dtype('f4')),
              'RADIUS_RS': pd.Series(col_rad_rs, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def gen_detcl_output(ra, dec, z):
    col_id = np.array(range(row_numbers))
    col_ra = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    col_dec = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    col_z = generate_vector(row_numbers, 'float', z['min'], z['max'])
    col_z_err = generate_vector(row_numbers, 'float', 0, 1)
    col_snr = generate_vector(row_numbers, 'float', 3.0, 80)
    col_snr_unique = generate_vector(row_numbers, 'float', 3.0, 80)
    col_rad = generate_vector(row_numbers, 'float', 0.5, 60)
    col_richness = generate_vector(row_numbers, 'float', 0, 1)
    col_lambda_star = generate_vector(row_numbers, 'float', 0, 1)
    col_edge = generate_vector(row_numbers, 'int', 0, 1)
    col_fraction_masked = generate_vector(row_numbers, 'float', 0, 1)
    
    matrix = {'ID_CLUSTER': pd.Series(col_id, dtype=np.dtype('i8')),
              'RIGHT_ASCENSION_CLUSTER': pd.Series(col_ra, dtype=np.dtype('f8')),
              'DECLINATION_CLUSTER': pd.Series(col_dec, dtype=np.dtype('f8')),
              'Z_CLUSTER': pd.Series(col_z, dtype=np.dtype('f4')),
              'Z_ERR_CLUSTER': pd.Series(col_z_err, dtype=np.dtype('f4')),
              'SNR_CLUSTER': pd.Series(col_snr, dtype=np.dtype('f4')),
              'SNR_UNIQUE_CLUSTER': pd.Series(col_snr_unique, dtype=np.dtype('f4')),
              'RADIUS_CLUSTER': pd.Series(col_rad, dtype=np.dtype('f4')),
              'RICHNESS_CLUSTER': pd.Series(col_richness, dtype=np.dtype('f4')),
              'LAMBDA_STAR_CLUSTER': pd.Series(col_lambda_star, dtype=np.dtype('f4')),
              'FLAG_EDGE_CLUSTER': pd.Series(col_edge, dtype=np.dtype('f4')),
              'FRAC_MASKED_CLUSTER': pd.Series(col_fraction_masked, dtype=np.dtype('f4'))}

    df = pd.DataFrame(matrix) 

    return df.to_records(index=False)

def clean_old_files(dirty_file):
    if os.path.exists(dirty_file): 
        os.remove(dirty_file)

import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem)
    reparsed = minidom.parseString(rough_string)
    string = reparsed.toprettyxml(indent="  ", encoding="UTF-8")
    return string.decode('utf-8') 

def fill_header(header):
    ET.SubElement(header, "ProductId").text= "61044e80-fed2-427b-aabf-c608980814a5"
    ET.SubElement(header, "ProductType").text= "TestProduct"
    ET.SubElement(header, "SoftwareName").text= "NA"
    ET.SubElement(header, "SoftwareRelease").text= "3.5"
    ET.SubElement(header, "EuclidPipelineSoftwareRelease").text= "0.0"
    ET.SubElement(header, "ProdSDC").text= "SDC-FR"
    ET.SubElement(header, "DataSetRelease").text= "NA"
    ET.SubElement(header, "Purpose").text= "UNKNOWN"
    ET.SubElement(header, "PlanId").text= "ec0f9326-5e57-4e36-af30-8b6352c1a650"
    ET.SubElement(header, "PPOId").text= "bbab3151-64b7-4155-b2d3-080fd84e3287"
    ET.SubElement(header, "PipelineDefinitionId").text= "PipelineDefinitionId"
    ET.SubElement(header, "PipelineRun").text= "NA"
    ET.SubElement(header, "ExitStatusCode").text= "NA"
    ET.SubElement(header, "ManualValidationStatus").text= "UNKNOWN"
    ET.SubElement(header, "ExpirationDate").text= "2020-07-09T10:48:43.495Z"
    ET.SubElement(header, "ToBePublished").text= "false"
    ET.SubElement(header, "Published").text= "false"
    ET.SubElement(header, "Curator").text= "Curator0"
    ET.SubElement(header, "CreationDate").text= "2020-07-09T10:48:43.495Z"

    return header

def create_xml(filepath_fits, filepath_xml, header_data, description_xml):
    ET.register_namespace('0', description_xml["catnamespace"])
    root = ET.Element("ns1:" + description_xml["catname"])
    root.set("xmlns:ns1", description_xml["catnamespace"])

    header = ET.SubElement(root, "Header")
    header = fill_header(header)
    data = ET.SubElement(root, "Data")

    if description_xml["parameters"]:
        parameters = ET.SubElement(data, description_xml["parameters"])
        for name, value in header_data.items():
            ET.SubElement(parameters, name).text = str(value)

    catalog = ET.SubElement(data, description_xml["catfile"])
    catalog.set("format", "le3.cl.input.cat")
    catalog.set("version", "0.1")

    data_container = ET.SubElement(catalog, "DataContainer")
    data_container.set("filestatus", "PROPOSED")
    filename = ET.SubElement(data_container, "Filename").text = filepath_fits
 
    with open(filepath_xml, "x") as f:
        f.write(prettify_xml(root))
    print(f'Created {filepath_xml}')
    return None

def clean_and_create_file(output_folder, filename):
    filepath_fits = os.path.join(output_folder, filename + '.fits')
    filepath_xml = os.path.join(output_folder, filename + '.xml')
    clean_old_files(filepath_fits)
    clean_old_files(filepath_xml)
    
    return filepath_fits, filepath_xml

def write_catalogs(filepath_fits, filepath_xml, data, header, description_xml):
    fitsio.write(filepath_fits, data, header=header)
    print(f'Created {filepath_fits}')
    create_xml(filepath_fits, filepath_xml, header, description_xml)

xml_description_det_cluster={"catname": "DpdLE3clDetClusters",
                             "catnamespace": "http://euclid.esa.org/schema/dpd/le3/cl/detdetections",
                             "parameters": "ParamsList",
                             "catfile": "ClustersFile",
                             "cattype": "le3.cl.det.output.clusters"}
xml_description_richness={"catname": "DpdLE3clRichness",
                             "catnamespace": "http://euclid.esa.org/schema/dpd/le3/cl/richrichness",
                             "parameters": "",
                             "catfile": "RichCLRichnessFile",
                             "cattype": "le3.cl.rich.output.richness"}
xml_description_zcl={"catname": "DpdLE3clZClOutput",
                             "catnamespace": "http://euclid.esa.org/schema/dpd/le3/cl/zcloutput",
                             "parameters": "",
                             "catfile": "ZClOutputFile",
                             "cattype": "le3.cl.zcl.output"}
xml_description_richmembers={"catname": "DpdLE3clRichMembers",
                             "catnamespace": "http://euclid.esa.org/schema/dpd/le3/cl/richmembership",
                             "parameters": "",
                             "catfile": "RichMembersFile",
                             "cattype": "le3.cl.rich.output.membership"}
xml_description_amicomembers={"catname": "DpdLE3clAssociations",
                             "catnamespace": "http://euclid.esa.org/schema/dpd/le3/cl/amicomembers",
                             "parameters": "ParamsList",
                             "catfile": "associationsAMICOClusters",
                             "cattype": "le3.cl.det.output.AMICOass"}

if __name__ == '__main__':
    # Constants
    RA = {'min': 0, 'max': 5}
    DEC = {'min': -2.5, 'max':2.5}
    Z = {'min': 0.1, 'max': 3} 
    row_numbers = 2 
    output_folder = os.path.join(os.getcwd(), 'det_rich_output')

    # Choose paths
    pzwav_file, pzwav_file_xml = clean_and_create_file(output_folder, 'pzwav_dummy')
    amico_file, amico_file_xml = clean_and_create_file(output_folder, 'amico_dummy')
    richcl_amico_file, richcl_amico_file_xml = clean_and_create_file(output_folder, 'richcl_amico_dummy')
    richcl_pzwav_file, richcl_pzwav_file_xml = clean_and_create_file(output_folder, 'richcl_pzwav_dummy')
    zcl_pzwav_file, zcl_pzwav_file_xml = clean_and_create_file(output_folder, 'zcl_pzwav_dummy')
    zcl_amico_file, zcl_amico_file_xml = clean_and_create_file(output_folder, 'zcl_amico_dummy')
    amico_membership_from_am_file, amico_membership_from_am_file_xml = clean_and_create_file(output_folder, 'amico_membership_from_am_dummy')
    amico_membership_from_rich_file, amico_membership_from_rich_file_xml = clean_and_create_file(output_folder, 'amico_membership_from_rich_dummy')
    pzwav_membership_file, pzwav_membership_file_xml = clean_and_create_file(output_folder, 'pzwav_membership_dummy')
    prof_file, prof_file_xml = clean_and_create_file(output_folder, 'prof_dummy')


    # Generate headers
    header_amico = gen_amico_header(RA, DEC, Z)
    header_pzwav = gen_pzwav_header(RA, DEC, Z)
    header_richcl_amico = gen_richcl_header(RA, DEC)
    header_richcl_pzwav = gen_richcl_header(RA, DEC)
    header_zcl_pzwav = gen_zcl_header()
    header_zcl_amico = gen_zcl_header()
    header_amico_membership_from_am = None 
    header_amico_membership_from_rich = None 
    header_pzwav_membership = None
    header_prof = gen_prof_header(RA, DEC, Z)
    
    # Generate data 
    data_amico = gen_detcl_output(RA, DEC, Z)
    data_pzwav = gen_detcl_output(RA, DEC, Z)
    data_richcl_amico = gen_richcl_output()
    data_richcl_pzwav = gen_richcl_output()
    data_zcl_pzwav = gen_zcl_output(Z)
    data_zcl_amico = gen_zcl_output(Z)
    data_amico_membership_from_am = gen_rich_amico_output()
    data_amico_membership_from_rich = None
    data_pzwav_membership = None
    data_prof = gen_prof_output(RA, DEC)

    # Write catalogs 
    write_catalogs(amico_file, amico_file_xml, data_amico, header_amico, xml_description_det_cluster)
    write_catalogs(pzwav_file, pzwav_file_xml, data_pzwav, header_amico, xml_description_det_cluster)
    write_catalogs(richcl_amico_file, richcl_amico_file_xml, data_richcl_amico, header_richcl_amico, xml_description_richness)
    write_catalogs(richcl_pzwav_file, richcl_pzwav_file_xml, data_richcl_pzwav, header_richcl_pzwav, xml_description_richness)
    write_catalogs(zcl_pzwav_file, zcl_pzwav_file_xml, data_zcl_pzwav, header_zcl_pzwav, xml_description_zcl)
    write_catalogs(zcl_amico_file, zcl_amico_file_xml, data_zcl_amico, header_zcl_amico, xml_description_zcl)
    write_catalogs(amico_membership_from_am_file, amico_membership_from_am_file_xml, data_amico_membership_from_am, header_amico, xml_description_amicomembers)
    write_catalogs(amico_membership_from_rich_file, amico_membership_from_rich_file_xml, data_amico_membership_from_rich, header_amico_membership_from_rich, xml_description_richmembers)
    write_catalogs(pzwav_membership_file, pzwav_membership_file_xml, data_pzwav_membership, header_pzwav_membership, xml_description_richmembers)
    write_catalogs(prof_file, prof_file_xml, data_prof, header_prof, xml_description_det_cluster)
