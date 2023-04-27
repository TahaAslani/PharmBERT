from scipy.stats import sem
import pandas as pd
import numpy as np
import sys
import os

seeds = [42, 555, 666, 999, 9999]

res_path = sys.argv[1]

def read_json(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    for line in lines[0].split(','):
        if line.startswith(" 'f1'"):
            f1 = float(line.split(': ')[-1].split('}')[0])
            
    return f1

F1_list = []

for seed in seeds:

    f1_path = os.path.join(res_path, str(seed), 'eval-'+average+'-.json')
    f1 = read_json(f1_path)
    F1_list.append(f1)

print('Mean F1', np.mean(F1_list))
print('Standard error F1', sem(F1_list))
