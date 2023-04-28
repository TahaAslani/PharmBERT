#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 23:27:58 2022

@author: taha
"""

import os
import sys
import numpy as np
from sklearn.metrics import f1_score

# folder = '/home/taha/Desktop'
folder = sys.argv[1]

preds = np.load(os.path.join(folder,'preds.npy'))
labels = np.load(os.path.join(folder,'labels.npy'))


generic_label = 0
interest_labels = list(set(labels))
interest_labels.remove(generic_label)

F1 = f1_score(labels, preds, labels=interest_labels, average='micro')
print('Cllassification F1-micro',F1)

F1_macro = f1_score(labels, preds, labels=interest_labels, average='macro')
print('Cllassification F1-macro',F1_macro)


f = open(os.path.join(folder,'MICRO-F1-CLASS.txt'),'w')
f.write(str(np.round(F1,5)))
f.write('\n')
f.close()


f = open(os.path.join(folder,'MACRO-F1-CLASS.txt'),'w')
f.write(str(np.round(F1_macro,5)))
f.write('\n')
f.close()


labels_DDI=labels[labels!=0]
preds_DDI=preds[labels!=0]

F1_r = f1_score(labels_DDI, preds_DDI, average='micro')
F1_macro_r = f1_score(labels_DDI, preds_DDI, average='macro')

f = open(os.path.join(folder,'MICRO-F1-REMOVE.txt'),'w')
f.write(str(np.round(F1_r,5)))
f.write('\n')
f.close()


f = open(os.path.join(folder,'MACRO-F1-REMOVE.txt'),'w')
f.write(str(np.round(F1_macro_r,5)))
f.write('\n')
f.close()


