import fitsio
import numpy as np
import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from astropy.table import Table

def generate_vector(length, num_type, mini, maxi, col_nb=1):

    if num_type is 'float':
        new_vector = np.random.random_sample((length, col_nb)) * (maxi - mini) + mini
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
    output = Table()
    
    output['ID_CLUSTER'] = np.array(range(row_numbers))
    output['Z_ZCL'] =generate_vector(row_numbers, 'float', z['min'], z['max'])
    output['Z_ZCL_ERR'] = generate_vector(row_numbers, 'float', 0, 1)

    return output 

def gen_prof_output(ra, dec):
    output = Table()
    
    output['ID_CLUSTER'] = np.array(range(row_numbers))
    output[ 'RA_CEN_BESTFIT'] = generate_vector(row_numbers, 'float', ra['min'], ra['max']) 
    output['DEC_CEN_BESTFIT'] = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    output['LOG_SCALE_RADIUS_BESTFIT'] = generate_vector(row_numbers, 'float', 0, 40) 
    output['ELLIPTICITY_BESTFIT']  = generate_vector(row_numbers, 'float', 0.5, 3)
    output['PA_BESTFIT']  = generate_vector(row_numbers, 'float', 0, 1)
    output['LOG_BACKGROUND_BESTFIT']  = generate_vector(row_numbers, 'float', 0, 1)
    output['NOFA_BESTFIT']  = generate_vector(row_numbers, 'float', 0, 1)
    output['MINUS_LOG_LIKELIHOOD'] = generate_vector(row_numbers, 'float', 0, 1)
    output['DEBLENDING_ORDER'] = generate_vector(row_numbers, 'float', 0, 1)
    output['BIC'] = generate_vector(row_numbers, 'float', 0, 1)
    output['FIT_NFEV'] = generate_vector(row_numbers, 'float', 0, 1)
    output['RA_CEN_GUESS'] = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    output['DEC_CEN_GUESS'] = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    output['LOG_SCALE_RADIUS_GUESS'] = generate_vector(row_numbers, 'float', 0, 1)
    output['ELLIPTICITY_GUESS'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PA_GUESS'] = generate_vector(row_numbers, 'float', 0, 1)
    output['LOG_BACKGROUND_GUESS'] = generate_vector(row_numbers, 'float', 0, 1)

    return output

def gen_rich_amico_output():
    output = Table()

    output['OBJECT_ID'] = generate_vector(row_numbers, 'int', 1, 10000)
    output['ID_CLUSTER'] = np.array(range(row_numbers))
    output['PMEM'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PMEM_ERR'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PMEM_RAD'] = generate_vector(row_numbers, 'float', 0, 40)
    output['PMEM_Z'] = generate_vector(row_numbers, 'float', 0.5, 3)
    output['PMEM_RS'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PMEM_RS_ERR'] = generate_vector(row_numbers, 'float', 0, 1)

    return output

def gen_rich_members_output():
    output = Table()

    output['OBJECT_ID'] = np.array(range(row_numbers))
    output['ID_CLUSTER'] = generate_vector(row_numbers, 'int', 1, 999999)
    output['PMEM'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PMEM_ERR'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PMEM_RAD'] = generate_vector(row_numbers, 'float', 1, 80)
    output['PMEM_Z'] = generate_vector(row_numbers, 'float', 1, 3000)
    output['PMEM_RS'] = generate_vector(row_numbers, 'float', 0, 1)
    output['PMEM_RS_ERR'] = generate_vector(row_numbers, 'float', 3.0, 80)

    return output 

def gen_richcl_output():
    output = Table()

    output['ID_CLUSTER'] = np.array(range(row_numbers))
    output['RICHNESS_VEC'] = generate_vector(row_numbers, 'float', 1, 3000, col_nb=300)
    output['RICHNESS_ERR_VEC'] = generate_vector(row_numbers, 'float', 1, 80, col_nb=300)
    output['RADIUS_VEC'] = generate_vector(row_numbers, 'float', 1, 80, col_nb=300)
    output['RICHNESS'] = generate_vector(row_numbers, 'float', 1, 3000)
    output['RICHNESS_ERR'] = generate_vector(row_numbers, 'float', 1, 80)
    output['RADIUS'] = generate_vector(row_numbers, 'float', 3.0, 80)
    output['BKG_FRACTION'] = generate_vector(row_numbers, 'float', 0, 1)
    output['RICHNESS_VEC_RS'] = generate_vector(row_numbers, 'float', 0, 10, col_nb=300)
    output['RICHNESS_ERR_VEC_RS'] = generate_vector(row_numbers, 'float', 0, 10, col_nb=300)
    output['RADIUS_VEC_RS'] = generate_vector(row_numbers, 'float', 0, 10, col_nb=300)
    output['RICHNESS_RS'] = generate_vector(row_numbers, 'float', 0, 10)
    output['RICHNESS_ERR_RS'] = generate_vector(row_numbers, 'float', 0, 10)
    output['RADIUS_RS'] = generate_vector(row_numbers, 'float', 0, 10)

    return output 

def gen_detcl_output(ra, dec, z):
    output = Table()
 
    output['ID_CLUSTER'] = np.array(range(row_numbers)) 
    output['RIGHT_ASCENSION_CLUSTER'] = generate_vector(row_numbers, 'float', ra['min'], ra['max'])
    output['DECLINATION_CLUSTER'] = generate_vector(row_numbers, 'float', dec['min'], dec['max'])
    output['Z_CLUSTER'] = generate_vector(row_numbers, 'float', z['min'], z['max'])
    output['Z_ERR_CLUSTER'] = generate_vector(row_numbers, 'float', 0, 1)
    output['SNR_CLUSTER']  = generate_vector(row_numbers, 'float', 3.0, 80)
    output['SNR_UNIQUE_CLUSTER'] = generate_vector(row_numbers, 'float', 3.0, 80)
    output['RADIUS_CLUSTER'] = generate_vector(row_numbers, 'float', 0.5, 60)
    output['RICHNESS_CLUSTER'] = generate_vector(row_numbers, 'float', 0, 1)
    output['LAMBDA_STAR_CLUSTER'] = generate_vector(row_numbers, 'float', 0, 1)
    output['FLAG_EDGE_CLUSTER'] = generate_vector(row_numbers, 'int', 0, 1)
    output['FRAC_MASKED_CLUSTER'] = generate_vector(row_numbers, 'float', 0, 1)

    return output 

def clean_old_files(dirty_file):
    if os.path.exists(dirty_file): 
        os.remove(dirty_file)

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

def create_xml(filepath_fits, filepath_xml, header_data, description_xml, keywords_params):
    ET.register_namespace('0', description_xml["catnamespace"])
    root = ET.Element("ns1:" + description_xml["catname"])
    root.set("xmlns:ns1", description_xml["catnamespace"])

    header = ET.SubElement(root, "Header")
    header = fill_header(header)
    data = ET.SubElement(root, "Data")

    if description_xml["parameters"]:
        parameters = ET.SubElement(data, description_xml["parameters"])
        for name in keywords_params:
            try:
                ET.SubElement(parameters, name[0]).text = str(header_data[name[0]])
            except KeyError:
                if name[1] == int:
                    ET.SubElement(parameters, name[0]).text = str(0)
                elif name[1] == bool:
                    ET.SubElement(parameters, name[0]).text = "False"

    catalog = ET.SubElement(data, description_xml["catfile"])
    catalog.set("format", description_xml["cattype"])
    catalog.set("version", "0.1")

    data_container = ET.SubElement(catalog, "DataContainer")
    data_container.set("filestatus", "PROPOSED")
    filename = ET.SubElement(data_container, "FileName").text = filepath_fits
 
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

def write_catalogs(filepath_fits, filepath_xml, data, header, description_xml, keywords_params):
    fitsio.write(filepath_fits, data.as_array(), header=header)
    print(f'Created {filepath_fits}')
    create_xml(filepath_fits, filepath_xml, header, description_xml, keywords_params)

keywords_params_detcl=[("MIN_Z", int), ("MAX_Z", int), ("MIN_RA", int), ("MAX_RA", int),
                       ("MIN_DEC", int), ("MAX_DEC", int), ("SNR_THR", int), ("CUBE_XY_STEP", int),
                       ("MAX_AREA_DEG", int), ("L_BORDER_DEG", int), ("DZ", int), ("ZSTEP", int),
                       ("KRN_SCL1", int), ("KRN_SCL2", int), ("DR_LIM", int), ("DZ_LIM", int),
                       ("FROM_DENSITY_MAP", bool), ("OMEGA_MAT", int), ("OMEGA_VAC", int),
                       ("HUBBLE_PAR", int), ("W_EQ_STATE", int), ("N_EFF", int), ("TEMP_CMB", int),
                       ("MAX_NB", int), ("MIN_PROB", int)]

keywords_params_richcl_richness=[("MIN_RA", int), ("MAX_RA", int), ("MIN_DEC", int), ("MAX_DEC", int),
                                 ("SNR_THR", int), ("MODEL_ID", int), ("MAX_NB", int), ("MIN_PROB", int)]
keywords_params_richcl_members=[("SNR_THR", int), ("MODEL_ID", int), ("MAX_NB", int), ("MIN_PROB", int)]
keywords_params_zcl = None

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
    header_amico_membership_from_am = gen_zcl_header() 
    header_amico_membership_from_rich = gen_zcl_header() 
    header_pzwav_membership = gen_zcl_header()
    header_prof = gen_prof_header(RA, DEC, Z)
    
    # Generate data 
    data_amico = gen_detcl_output(RA, DEC, Z)
    data_pzwav = gen_detcl_output(RA, DEC, Z)
    data_richcl_amico = gen_richcl_output()
    data_richcl_pzwav = gen_richcl_output()
    data_zcl_pzwav = gen_zcl_output(Z)
    data_zcl_amico = gen_zcl_output(Z)
    data_amico_membership_from_am = gen_rich_amico_output()
    data_amico_membership_from_rich = gen_rich_members_output()
    data_pzwav_membership = gen_rich_members_output()
    data_prof = gen_prof_output(RA, DEC)

    # Write catalogs 
    write_catalogs(amico_file, amico_file_xml, data_amico, header_amico, xml_description_det_cluster, keywords_params_detcl)
    write_catalogs(pzwav_file, pzwav_file_xml, data_pzwav, header_amico, xml_description_det_cluster, keywords_params_detcl)
    write_catalogs(richcl_amico_file, richcl_amico_file_xml, data_richcl_amico, header_richcl_amico, xml_description_richness, keywords_params_richcl_richness)
    write_catalogs(richcl_pzwav_file, richcl_pzwav_file_xml, data_richcl_pzwav, header_richcl_pzwav, xml_description_richness, keywords_params_richcl_richness)
    write_catalogs(zcl_pzwav_file, zcl_pzwav_file_xml, data_zcl_pzwav, header_zcl_pzwav, xml_description_zcl, keywords_params_zcl)
    write_catalogs(zcl_amico_file, zcl_amico_file_xml, data_zcl_amico, header_zcl_amico, xml_description_zcl, keywords_params_zcl)
    write_catalogs(amico_membership_from_am_file, amico_membership_from_am_file_xml, data_amico_membership_from_am, header_amico, xml_description_amicomembers, keywords_params_detcl)
    write_catalogs(amico_membership_from_rich_file, amico_membership_from_rich_file_xml, data_amico_membership_from_rich, header_amico_membership_from_rich, xml_description_richmembers, keywords_params_richcl_members)
    write_catalogs(pzwav_membership_file, pzwav_membership_file_xml, data_pzwav_membership, header_pzwav_membership, xml_description_richmembers, keywords_params_richcl_members)
    write_catalogs(prof_file, prof_file_xml, data_prof, header_prof, xml_description_det_cluster, keywords_params_detcl)
