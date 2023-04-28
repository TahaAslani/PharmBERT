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

f = open(os.path.join(folder,'MICRO-F1.txt'),'w')
f.write(str(np.round(F1,5)))
f.write('\n')
f.close()
