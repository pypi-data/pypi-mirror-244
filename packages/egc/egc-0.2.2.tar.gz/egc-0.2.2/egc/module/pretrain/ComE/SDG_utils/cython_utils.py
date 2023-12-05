"""
Used to place .pyx file generation system executable binary file
"""
import os

import numpy
from Cython.Build import cythonize
from distutils.core import setup

if __name__ == "__main__":
    basename = os.path.abspath(
        f"{os.path.dirname(os.path.realpath(__file__))}")
    setup(
        name="SDG app",
        ext_modules=cythonize(
            f"{basename}/training_sdg_inner.pyx",
            compiler_directives={
                "boundscheck": False,
                "wraparound": False,
                "cdivision": True,
            },
        ),
        include_dirs=[numpy.get_include()],
    )

#
# 1. Install Cython==0.25
# 2. In comE-master, run: 'python3 cython_utils.py build_ext'
# 3. A new directory 'build' will be created.
# Navigate the directories and find training_sdg_inner.cpython-36m-x86_64-linux-gnu.so
# and training_sdg_inner.o. Copy and paste both files to the comE-master/utils/ directory.
# 4. run: 'python3 main.py'
# You can also edit main.py to change the parameters at your will.
