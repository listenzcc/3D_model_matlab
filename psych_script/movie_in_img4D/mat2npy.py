# coding: utf-8

import numpy as np
import scipy.io as sio

for motion_name in ['quzhou', 'shenchu', 'taiqi', 'waizhan']:
    mat = sio.loadmat('%s.mat' % motion_name)
    d = mat['movie_4D']
    np.save('%s.npy' % motion_name, d)
