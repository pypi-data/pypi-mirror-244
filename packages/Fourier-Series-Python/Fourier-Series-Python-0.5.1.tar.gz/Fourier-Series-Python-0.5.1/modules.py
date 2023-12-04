import Fourier as f
import Generate as Signal
import numpy as np
import pandas as pd
from ipywidgets import interact
from FunctionDefinitions import *
from Plot import *
import numpy as np
#import tensorflow as tf
np.seterr(divide='ignore', invalid='ignore')
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


N = [15,20,40,45,80,135,160,320,405,640,1215,1280,1500]

f.calculateIdftMat(N)
fig=go.Figure()