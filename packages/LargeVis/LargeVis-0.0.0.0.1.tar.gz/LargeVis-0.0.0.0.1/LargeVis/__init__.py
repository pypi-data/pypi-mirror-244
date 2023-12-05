
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import os,sys,stat
print(os.getcwd())
path0=os.getcwd()
# help(os.chdir)
#os.chdir(r"D:\AAAA_learning\Bioinformatics_advanced")
print(path0)
import pandas as pd
import scipy.sparse as ss
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.base import BaseEstimator
from sklearn.utils import check_array
from os.path import isfile
import subprocess
import os, pkg_resources
import pandas as pd
#from subprocess import check_call
classpath0 = (pkg_resources.resource_filename("LargeVis", ""))
print(classpath0)
os.chdir(classpath0)
print(os.getcwd())
data_dir="LargeViscpp"
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)
else:
    print(data_dir,'directory already exists.')
print("please wait seveal minutes,and the C++ file is downloading")    
import urllib.request
data_url="https://raw.githubusercontent.com/wangzichenbioinformatics/LargeVis/main/LargeVis2"
data_file_path="LargeViscpp/LargeVis"
if not os.path.isfile(data_file_path):
    result = urllib.request.urlretrieve(data_url,data_file_path)
else:
    print(data_file_path,'data file already exists.')    

classpath = (pkg_resources.resource_filename("LargeVis", "LargeViscpp/LargeVis"))
print(classpath)
os.chmod(classpath,stat.S_IRWXO)
os.chdir(path0)
print(os.getcwd())
from sklearn.base import BaseEstimator
class LargeVis (BaseEstimator):
    
    def __init__(self, n_components=2, perplexity=50.0, gamma=5,
                 layout_samples=None, n_neighbors=None, negative_samples=5,
                 alpha=1.0, n_cores=4, knn_prop=3, trees=50):
        self.n_components = n_components
        self.perplexity = perplexity
        self.layout_samples = layout_samples
        self.alpha = alpha
        self.n_cores = n_cores
        self.knn_prop = knn_prop
        self.negative_samples = negative_samples
        self.n_neighbors = n_neighbors
        self.gamma = gamma
        self.trees = trees
        if self.n_neighbors is None:
            self.n_neighbors = int(self.perplexity * 3)


    def fit_transform(self, X, y=None):
        
        if self.layout_samples is None:
            layout_samples = X.shape[0] / 100.0
        else:
            layout_samples = self.layout_samples
            
        X = check_array(X, dtype=np.float64)
        np.savetxt('/tmp/largevis_input', 
                   X, header='{} {}'.format(*X.shape), 
                   comments='')
        subprocess.check_call([classpath,
                               '-input', '/tmp/largevis_input',
                               '-output', '/tmp/largevis_output',
                               '-outdim', str(self.n_components),
                               '-perp', str(self.perplexity),
                               '-samples', str(layout_samples),
                               '-gamma', str(self.gamma),
                               '-prop', str(self.knn_prop),
                               '-trees', str(self.trees),
                               '-neigh', str(self.n_neighbors),
                               '-alpha', str(self.alpha),
                               '-neg', str(self.negative_samples),
                               '-threads', str(self.n_cores)])
        self.embedding_ = np.loadtxt('/tmp/largevis_output', skiprows=1)
        return self.embedding_
    
    def fit(self, X, y=None):
        self.fit_transform(X)
        return self	
	
	
	
