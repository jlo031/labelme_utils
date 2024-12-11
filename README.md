# labelme_utils

Library with utils to convert json files that were created with *labelme* to training masks in the original image geometry.

### Setup
First create and anaconda environment with gdal and labelme installed:

    # create and activate new environment
    conda create -y -n LABELME gdal
    conda activate LABELME

    # install required packages
    conda install -y loguru
    pip install ipython
    pip install labelme

Then install the current version of *labelme_utils*:

    # install this package
    pip install git+https://github.com/jlo031/labelme_utils

### Test
Run the script *test_json_conversion.py* from the provided test folder.
