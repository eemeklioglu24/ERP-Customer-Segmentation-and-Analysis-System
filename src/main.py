import numpy as np
import matplotlib.pyplot as plt

import data_handler as dt
import functions as fc

X, N= dt.generate_random()
#dt.plot_X(X)
K = 4
dt.plot_X(X)
fc.plot_clusters(X, N, K)
fc.get_obj(X, N)