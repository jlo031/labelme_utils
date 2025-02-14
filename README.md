# labelme_utils

Library with utils to convert json files that were created with *labelme* to training masks in the original image geometry.


### Preparation
Create anaconda environment with gdal and labelme:

    # create and activate new environment
    conda create -y -n LABELME gdal
    conda activate LABELME

    # install required packages
    conda install -y loguru
    pip install ipython
    pip install labelme


### Installation
You can install this library directly from github (1) or locally after cloning (2).  
For both installation options, first set up the environment as described above.

1. **Installation from github**

       # install this package
       pip install git+https://github.com/jlo031/labelme_utils

2. **Local installation**

       # clone the repository
       git clone git@github.com:jlo031/labelme_utils

   Change into the main directory of the cloned repository (it should contain the *setup.py* file) and install the library:

       # installation
       pip install .


### Test
Run the script *test_json_conversion.py* from the provided test folder.
