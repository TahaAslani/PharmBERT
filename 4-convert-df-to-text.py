import os
import re
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Convert data frame to text')

parser.add_argument('--data-path', '-i', required=True, type=str,
    help='Data path.')
parser.add_argument('--output-path', '-o', required=True, type=str,
    help='Output path.')

args = parser.parse_args()

data_path = args.data_path
output_path = args.output_path

# Chosen columns
chosen_col = ['INDICATIONS_AND_USAGE', 'DOSAGE_AND_ADMINISTRATION', 'DOSAGE_FORMS_AND_STRENGTHS',
        'CONTRAINDICATIONS', 'WARNINGS_AND_PRECAUTIONS', 'ADVERSE_REACTIONS', 'DRUG_INTERACTIONS',
        'USE_IN_SPECIFIC_POPULATIONS', 'DRUG_ABUSE_AND_DEPENDENCE', 'OVERDOSAGE', 'DESCRIPTION',
        'CLINICAL_PHARMACOLOGY', 'NONCLINICAL_TOXICOLOGY', 'CLINICAL_STUDIES', 'HOW_SUPPLIED',
        'PATIENT_COUNSELING_INFORMATION', 'BOXED_WARNING',
        'CARCINOGENESIS_AND_MUTAGENESIS_AND_IMPAIRMENT_OF_FERTILITY',
        'FEMALES_AND_MALES_OF_REPRODUCTIVE_POTENTIAL', 'INFORMATION_FOR_PATIENTS',
        'PHARMACODYNAMICS', 'PHARMACOGENOMICS', 'PHARMACOKINETICS', 'PREGNANCY',
        'MECHANISM_OF_ACTION', 'NONTERATOGENIC_EFFECTS', 'NURSING_MOTHERS',
        'LACTATION', 'TERATOGENIC_EFFECTS', 'SPL_PATIENT_PACKAGE_INSERT']

# Load the data
df = pd.read_csv(data_path)

# Print every 10000 steps
print_step = 10000

f = open(output_path,'w')

# Clean the text
def clean_up(string):
    string = re.sub('\\\\x..', '', string)
    string = re.sub('\\\\t', '', string).strip()
    # string = re.sub(r'\s+', ' ', string)
    return string

for i in df.index:
    
    for col in chosen_col:

       	if not pd.isnull(df.loc[i,col]):

            f.write(clean_up(df.loc[i,col]))
            f.write('\n')

    if i % print_step == 0:
        print('Finished', i,'out of',df.shape[0])
    
f.close()

print('Done!')
