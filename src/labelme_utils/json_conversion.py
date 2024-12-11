# ---- This is <json_conversion.py.py> ----

"""
Processing of json files with labeled data from labelme library.
""" 

import sys
import pathlib
import json

import labelme

from loguru import logger
from osgeo import gdal

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_class_name_list_from_labels_txt(labels_path):
    """
    Create a list of class names from input labels.txt file.

    Parameters
    ----------
    labels_path : path to labels text file with class labels

    Returns
    -------
    class_names : list of class names
    """

    labels_path  = pathlib.Path(labels_path).resolve()

    if not labels_path.exists():
        logger.error(f'Cannot find labels_path: {labels_path}')
        return

    # read class names from labels_path
    with open(labels_path.as_posix()) as f:
        class_names = f.read().splitlines()

    return class_names

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_class_name_list_from_json_file(json_path):
    """
    Create a list of class names from input json file.

    Parameters
    ----------
    json_path : path to input json file

    Returns
    -------
    class_names : list of class names
    """

    json_path  = pathlib.Path(json_path).resolve()

    if not json_path.exists():
        logger.error(f'Cannot find json_path: {json_path}')
        return


    # load json file
    with open(json_path.as_posix()) as f:
        data = json.load(f)

    class_names_in_json_file = []

    for i, shape in enumerate(data['shapes']):
        logger.debug(f'Checking shape numnber {i}')
        logger.debug(f'Current shape label is: {shape['label']}')
        class_names_in_json_file.append(shape['label'])
    
    class_names = list(set(class_names_in_json_file))

    return class_names

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_label_index_mapping(class_names):
    """
    Map label names to numbers that can be used for classification.

    Parameters
    ----------
    class_names : list of class name strings

    Returns
    -------
    label_index_mapping : dict with label names (key) and numbers (value)
    """

    # initialise the label dict
    label_index_mapping = dict()

    # loop through all class names and add entry to dict
    for idx, name in enumerate(class_names):
        label_index_mapping[name] = idx + 1

    return label_index_mapping

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def load_training_shapes(json_path, label_index_mapping=None):
    """
    Load training shapes points from input json file.

    Parameters
  ----------
    json_path : path to input json file
    label_index_mapping : dict with label names (key) and class index (value)

    Returns
    -------
    shapes : list with dict entry for each polygon shape in json file
    label_index_dict : dict with label names (key) and class index (value)
    """

    json_path  = pathlib.Path(json_path).resolve()

    if not json_path.exists():
        logger.error(f'Cannot find json_path: {json_path}')
        return

    # set background value for label mask
    label_index_dict = {'_background_': 0}

    # if no explicit mapping given, simply assign increasing non-zero numbers to the labels from the json file
    if label_index_mapping is None:
        class_labels = get_class_name_list_from_json_file(json_path)
        label_index_mapping= get_label_index_mapping(class_names)

    # 0 cannot be in the label_index_mapping
    assert 0 not in label_index_mapping.values(), 'Zero label is reserved for background!'

    # combine background and label_index_mapping
    label_index_dict.update(label_index_mapping)


    # load json file
    with open(json_path) as f:
        data = json.load(f)

    # get polygon shapes
    shapes = list(filter(lambda s: s['label'] in label_index_mapping, data['shapes']))

    return shapes, label_index_dict

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_label_image(json_path, label_index_mapping=None):
    """
    Create a mask image from input labelme json file.

    Parameters
    ----------
    json_path : path to input json file
    label_index_mapping : dict with label names (key) and class index (value)

    Returns
    -------
    label_image : array in image geometry with label values
    label_index_dict : dict with label names (key) and class index (value)
    """

    json_path  = pathlib.Path(json_path).resolve()

    if not json_path.exists():
        logger.error(f'Cannot find json_path: {json_path}')
        return


    # load shapes
    shapes, label_index_dict = load_training_shapes(json_path, label_index_mapping)

    # load json file
    with open(json_path) as f:
        data = json.load(f)

    # check for different formatting (version dependent) of labelme json file and read img_shape
    if 'imageDataShape' in data.keys():
        img_shape = data['imageDataShape']
    elif 'imageHeight' in data.keys() and 'imageWidth' in data.keys():
        img_shape = [data['imageHeight'], data['imageWidth']]

    # use internal labelme.utils to create label image
    # returns a tuple:
    # 1st image has class labels, 2nd image has running numbers of polygons
    label_image, polygon_image = labelme.utils.shapes_to_label(img_shape, shapes, label_index_dict)

    return label_image, polygon_image, label_index_dict

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def convert_json_file_2_mask(json_path, labels_path, train_folder, output_format='ENVI', overwrite=False, loglevel='INFO'):
    """
    Convert training json file to training mask and save in output folder.

    Parameters
    ----------
    json_path : path to input json file
    labels_path : path to labels text file with class labels
    train_folder : path to output folder where training mask images are placed
    output_format : image format for output file ('ENVI' or 'GTiff')
    overwrite : overwrite existing files (default=False)
    loglevel : loglevel setting (default='INFO')
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    logger.info('Converting training json file to training mask')

    logger.debug(f'{locals()}')
    logger.debug(f'file location: {__file__}')

    # get directory where module is installed
    module_path = pathlib.Path(__file__).parent.parent
    logger.debug(f'module_path: {module_path}')

# -------------------------------------------------------------------------- #

    # convert folder strings to paths
    json_path    = pathlib.Path(json_path).resolve()
    labels_path  = pathlib.Path(labels_path).resolve()
    train_folder = pathlib.Path(train_folder).resolve()

    logger.debug(f'json_path:    {json_path}')
    logger.debug(f'labels_path:  {labels_path}')
    logger.debug(f'train_folder: {train_folder}')

    if not json_path.exists():
        logger.error(f'Cannot find json_path: {json_path}')
        return

    if not labels_path.exists():
        logger.error(f'Cannot find labels_path: {labels_path}')
        return

    if not train_folder.is_dir():
        logger.warning(f'Output folder does not exist. Creating new output folder: {train_folder}')
        train_folder.mkdir(parents=True, exist_ok=True)

    if not output_format in ['ENVI', 'GTiff']:
        logger.error('Supported output formats are ENVI and GTiff')
        return

# -------------------------------------------------------------------------- #

    # get image basename from json_path
    f_base = json_path.stem.split('_scaled')[0]

    # define output file name and path
    if output_format == 'ENVI':
        output_path = train_folder / f'{f_base}_training_mask.img'
    elif output_format == 'GTiff':
        output_path = train_folder / f'{f_base}_training_mask.tiff'

    ##output_hdr_path = train_folder / f'{f_base}_training_mask.hdr'

    logger.debug(f'f_base:      {f_base}')
    logger.debug(f'output_path: {output_path}')


    # check if outfiles already exist
    if output_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return

# -------------------------------------------------------------------------- #

    # read class names from labels_path
    class_names = get_class_name_list_from_labels_txt(labels_path.as_posix())

    # create a dict that matches class names to numbers
    label_index_mapping = get_label_index_mapping(class_names)

    # load labels from json file
    label_image, polygon_image, label_index_dict = get_label_image(json_path, label_index_mapping)

# -------------------------------------------------------------------------- #

    # write to disk

    n_bands = 1
    Ny, Nx = label_image.shape

    # write to ENVI
    if output_format == 'ENVI':
        output = gdal.GetDriverByName('ENVI').Create(output_path.as_posix(), Nx, Ny, n_bands, gdal.GDT_Byte)
        output.GetRasterBand(1).WriteArray(label_image)

    # write to GTiff
    elif output_format == 'GTiff':
        output = gdal.GetDriverByName('GTiff').Create(output_path.as_posix(), Nx, Ny, n_bands, gdal.GDT_Byte)
        output.GetRasterBand(1).WriteArray(label_image)

    output.FlushCache()
    output = None

    return

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <json_conversion.py> ----
