# ---- This is <test_json_conversion.py> ----

"""
Test functions from labelme_utils.json_conversion library
"""

import labelme_utils.json_conversion as lm_json
import pathlib

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

labels_path  = pathlib.Path('./labels.txt')
json_path    = pathlib.Path('./test_image.json')
train_folder = pathlib.Path('./training_masks')

# -------------------------------------------------------------------------- #

# --------------------------------------- #
# Test "get_class_name_list_from_labels_txt
# --------------------------------------- #

class_names = lm_json.get_class_name_list_from_labels_txt(labels_path)
print(f'Read class_names from labels file: {class_names}')

# -------------------------------------------------------------------------- #

# ----------------------------------------- #
# Test "get_class_name_list_from_json_file" #
# ----------------------------------------- #

class_names = lm_json.get_class_name_list_from_json_file(json_path)
print(f'Read class_names from json file: {class_names}')

# -------------------------------------------------------------------------- #

# ------------------------------ #
# Test "get_label_index_mapping" #
# ------------------------------ #

label_index_mapping= lm_json.get_label_index_mapping(class_names)
print(f'Created label_index_mapping from class_names: {label_index_mapping}')

# -------------------------------------------------------------------------- #

# --------------------------- #
# Test "load_training_shapes" #
# --------------------------- #

shapes, label_index_dict = lm_json.load_training_shapes(json_path, label_index_mapping)

# -------------------------------------------------------------------------- #

# ----------------------- #
# Test "make_label_image" #
# ----------------------- #

label_image, polygon_image, label_index_dict = lm_json.get_label_image(json_path, label_index_mapping)

# -------------------------------------------------------------------------- #

# ------------------------------- #
# Test "convert_json_file_2_mask" #
# ------------------------------- #

lm_json.convert_json_file_2_mask(
    json_path, labels_path, train_folder, output_format='ENVI', overwrite=True, loglevel='INFO'
)

lm_json.convert_json_file_2_mask(
    json_path, labels_path, train_folder, output_format='GTiff', overwrite=False, loglevel='INFO'
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <test_json_conversion.py> ----


