##############################################
PROJECT_NAME="qinst"
VERSION="0.0.1"
DESC="Quantum experiments related works instruments" ;
##############################################


from setuptools import find_packages, setup
#from distutils.core import setup

from Cython.Distutils import build_ext
from distutils.extension import Extension
from setuptools.command.build_py import build_py as _build_py
import shutil ; 
import pathlib  ; 
import os ; 

if("nt" == os.name) : 
    os_slash= '\\' ;
else : 
    os_slash = '/'

with open("README.md", "r") as f:
    long_description = f.read()

def mkdir(path):
  pathlib.Path(path).mkdir(parents=True, exist_ok=True);

def slash(path):
  if(len(path) > 0 and path[-1]!="/"):path+="/";
  return path ; 

import sys ; 
vrs = sys.version.split(" ")[0].split('.') ; 
num  = vrs[0]+vrs[1] ; 

BIN_TARGETS = [
  "qcirc.schedule" ,
]


TARGETS  = [] ; 
for b in BIN_TARGETS : 
    c=b.replace('.' , os_slash)
    c+=".py";
    print(c)
    TARGETS.append([b,[c]])

##################################
print(TARGETS)

##################################
SOURCES = []; 
for t in TARGETS: 
  SOURCES+=t[1];
class build_py(_build_py):
  def byte_compile(self, files):
    _build_py.byte_compile(self, files)
    global SOURCES ; 
    print("######################################")
    for f in files:
      print(f);
      fp=os_slash.join(f.split(os_slash)[2:])
      if(fp in SOURCES) :
        os.unlink(f);
      #print(f.split(slash)[:2])

    print("######################################")


ext_modules  = [] ; 
for t in TARGETS : 
  ext_modules.append(
    Extension(t[0] , t[1])
  );  

setup(
    name=PROJECT_NAME,
    version="1.0.1",
    description=DESC,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OrkeshNurbolat",
    author_email="MG1922077@smail.nju.edu.cn",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    cmdclass = {"build_py":build_py , "build_ext" : build_ext } , 
    ext_modules = ext_modules
)

###################################################################################333
#### direct copy


OPEN_TARGETS = [
  #os_slash.join( ["rclab" , "Manual"  , "view.pdf" ])  , 
  #os_slash.join( ["rclab" , "DataView"  , "run.py" ])  ,
]

temp_dir=sys.argv[-1] ; 
for src in OPEN_TARGETS :  
  dest = os_slash.join( [ temp_dir ,src  ] ) ; 
  dr = pathlib.Path(dest).parent 
  mkdir(dr) ; 
  shutil.copyfile(src, dest);


