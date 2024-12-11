import labelme_utils as lm_utils

import sys
import pathlib
import json

import labelme

from loguru import logger
from osgeo import gdal


labels_path = '../../lc-ice/config/labels_winter.txt'
json_path = '/media/johannes/EO_disk/data/LC_ICE/crops/scaled_images/north_greenland_wb_237_L_scaled.json'
train_folder = './.'


# --------------------------------------- #
# Test "get_class_name_list_from_labels_txt
# --------------------------------------- #

class_names = lm_utils.get_class_name_list_from_labels_txt(labels_path)
print(f'Read class_names from labels file: {class_names}')

# ------------------------------------------------------------------- #

# ----------------------------------------- #
# Test "get_class_name_list_from_json_file" #
# ----------------------------------------- #

class_names = lm_utils.get_class_name_list_from_json_file(json_path)
print(f'Read class_names from json file: {class_names}')

# ------------------------------------------------------------------- #

# ------------------------------ #
# Test "get_label_index_mapping" #
# ------------------------------ #

label_index_mapping= lm_utils.get_label_index_mapping(class_names)
print(f'Created label_index_mapping from class_names: {label_index_mapping}')

# ------------------------------------------------------------------- #

# --------------------------- #
# Test "load_training_shapes" #
# --------------------------- #

shapes, label_index_dict = lm_utils.load_training_shapes(json_path, label_index_mapping)

# ------------------------------------------------------------------- #

# ----------------------- #
# Test "make_label_image" #
# ----------------------- #

label_image, polygon_image, label_index_dict = lm_utils.get_label_image(json_path, label_index_mapping)

# ------------------------------------------------------------------- #

# ------------------------------- #
# Test "convert_json_file_2_mask" #
# ------------------------------- #

lm_utils.convert_json_file_2_mask(
    json_path, labels_path, train_folder, output_format='ENVI', overwrite=True, loglevel='INFO'
)

lm_utils.convert_json_file_2_mask(
    json_path, labels_path, train_folder, output_format='GTiff', overwrite=False, loglevel='INFO'
)
