from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import shutil ; 
import pathlib  ; 
import os; 

def mkdir(path):
  pathlib.Path(path).mkdir(parents=True, exist_ok=True);

def slash(path):
  if(len(path) > 0 and path[-1]!="\\"):path+="\\";
  return path ; 


import sys ; 
vrs = sys.version.split(" ")[0].split('.') ; 
num  = vrs[0]+vrs[1] ; 

ext_txt = f".cp{num}-win_amd64.pyd";

TARGETS=  [
  [ "base_root"   , "Base"  ],
  [ "servers", "Base"],
  [ "common" , "Utils"],
  [ "pltr"   , "Utils"]  ,
  [ "rwdata" , "Utils"] , 
  [ "rwjson" , "Utils"] , 
  [ "tracer" , "Utils"], 
  [ "loadcsv" , "Utils"], 
  [ "Instrument" , "Instruments"], 
  [ "log_browser" , "DataView"]  ,  
  [ "adj" , "Utils/multiploter"] ,   
  [ "conf" , "Utils/multiploter"],    
  [ "ds" , "Utils/multiploter"]  ,  
  [ "mulpltr" , "Utils/multiploter"]    ,
  [ "ploter" , "Utils/multiploter"]   ,
  [ "que" , "Utils/multiploter"]    
]

SOURCE=[
  ["view.pdf" , "Manual"],
  ["requirements.txt" , ""]  ,
  ["__VERSION__.txt" , ""]  ,
  ["__init__.py" , ""]  ,
  ["run.py" , "DataView"] ,  
]

ext_modules  = [] ; 
for t in TARGETS : 
  ext_modules.append(
    Extension(t[0] , [slash(t[1])+t[0]+".py" ])
  ) ;  

setup(
  name  = "A test program" ,
  cmdclass = {"build_ext" : build_ext} , 
  ext_modules = ext_modules
)

target_dir = "Libraries\\NLab" ;
mkdir(target_dir) ;

for t in TARGETS: 
  dest_dir = slash(target_dir) + t[1]; 
  fn = t[0]  + ext_txt ; 
  mkdir(dest_dir);
  shutil.copyfile(fn , slash(dest_dir) + fn)

for t in SOURCE: 
  dest_dir = slash(target_dir) + t[1]; 
  fn =  t[0] ; 
  mkdir(dest_dir);
  shutil.copyfile(slash(t[1]) +fn , slash(dest_dir) + fn)


