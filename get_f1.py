from scipy.stats import sem
import pandas as pd
import numpy as np
import sys
import os

# differetn seeds
seeds = [42, 555, 666, 999, 9999]

# get the directory
res_path = sys.argv[1]

# Read json file
def read_json(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    for line in lines[0].split(','):
        if line.startswith(" 'f1'"):
            f1 = float(line.split(': ')[-1].split('}')[0])
            
    return f1

# Collect F1 of differetn seeds
F1_list = []
for seed in seeds:

    f1_path = os.path.join(res_path, str(seed), 'eval-micro-.json')
    f1 = read_json(f1_path)
    F1_list.append(f1)

# Report
print('Mean F1', np.mean(F1_list))
print('Standard error F1', sem(F1_list))
