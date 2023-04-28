from transformers import BertTokenizer
import pandas as pd
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--data_path', '-d', help="Path to  data folder", type=str)
parser.add_argument('--model_path', '-m', help="Path to model folder", type=str)
parser.add_argument('--output_path', '-o', help="Path to output folder", type=str)
args = parser.parse_args()
print(args)
input_dir = args.data_path
model_path = args.model_path
output_dir = args.output_path


# The label that is used for general text (no label)
none_label = str(0)

# Create output folder
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained(model_path)

# Convert a python list to a string format of json
def list2str(my_list):
    my_str = '['
    for element in my_list:
        my_str = my_str + '"' + str(element).replace('"', '\\"') + '", '
    my_str = my_str[:-2]+']'
    return my_str

# This function takes a none named entity (NE) text, tokenizes it and adds tekens to the
# global variable token. it will also add the lables of the same length to 
# the global variable ner_tags (labels). Since the text by defination is 
# none NE (no named entity, i.e. general text), all of the lables are
# general text (no label)
def handle_none_NE_chunk(chunk_text, final_chunk=False):
    
    global tokens, ner_tags
    
    chunk_splits = chunk_text.split('\n')
    for i,chunk_split in enumerate(chunk_splits):
        
        # Skip empty lines
        if len(chunk_split) == 0:
            continue
        
        chunk_tokens = tokenizer.tokenize(chunk_split)
        tokens += chunk_tokens
        ner_tags += [none_label] * len(chunk_tokens)
        
        # Do not end part if this is the last split (unless final chunk)
        if i==len(chunk_splits)-1 and (not final_chunk): # if last split
            continue
        
        # Skip empty data
        if len(tokens)==0:
            continue
        
        f.write('{')
        f.write('"words": '+list2str(tokens) + ', ')
        # print(len(tokens))
        f.write('"ner": '+list2str(ner_tags))
        f.write('}\n')
        
        tokens = []
        ner_tags = []
    
    return 0

# Run the code for train and test data

for partition in ['train', 'test']:
    
    f = open(os.path.join(output_dir, partition+'.json'), 'w')
    
    partition_input_path = os.path.join(input_dir, partition)
    
    files = os.listdir(partition_input_path)
    
    label_section_names = set([])
    for file in files:
        if file.split('.')[1] == 'ann' or file.split('.')[1] == 'txt':
            label_section_names.add(file.split('.')[0])
    
    for label_section_name in label_section_names:
        
        print(partition, label_section_name)
        
        ann_path = os.path.join(partition_input_path, label_section_name+'.ann')
        txt_path = os.path.join(partition_input_path, label_section_name+'.txt')
        
        text = open(txt_path, 'r').read()
        
        try:
            ANN = pd.read_csv(ann_path, header=None, sep='\t')
        except:
            if os.stat(ann_path).st_size == 0:
                ANN = pd.DataFrame(columns=['id', 'label', 'positions', 'str'])
                print('Empty data frame!')
            else:
                raise Exception(ann_path+' has an issue!')
        
        section_mentions_raw = ANN.loc[ANN.iloc[:,2].notnull(),:]
        
        section_mentions = pd.DataFrame(columns=['id', 'label', 'positions', 'str'])
        for i in section_mentions_raw.index:
            section_mentions.loc[i,'id'] = section_mentions_raw.iloc[i,0]
            section_mentions.loc[i,'label'] = section_mentions_raw.iloc[i,1].split(' ')[0]
            positions = ' '.join(section_mentions_raw.iloc[i,1].split(' ')[1:])
            section_mentions.loc[i,'positions'] = positions 
            section_mentions.loc[i,'str'] = section_mentions_raw.iloc[i,2]
            
        # Sort by mention position:
        def split_int(my_string):
            return int(my_string.split(' ')[0])
        start_positins = section_mentions.loc[:,'positions'].apply(split_int)
        section_mentions['start_positins'] = start_positins
        
        section_mentions.sort_values('start_positins', ignore_index=True, inplace=True)
        
        tokens = []
        ner_tags = []
        
        pos = 0
        for i in section_mentions.index:    
            # print()
            # print(text[int(NE_start_text[0]):int(NE_start_text[0])+int(NE_len_text[0])])
            # print(section_mentions.loc[i,'str'])
            
            positions = section_mentions.loc[i,'positions']
            positions = positions.split(';')
            
            for counter in range(len(positions)):
                
                NE_start = int(positions[counter].split(' ')[0])
                NE_end = int(positions[counter].split(' ')[1])
                
                # None NE
                # print(pos, NE_start, NE_end)
                chunk_text = text[pos:NE_start]
                handle_none_NE_chunk(chunk_text)
        
                # print('NNE', chunk_tokens)
                
                # NE
                chunk_text = text[NE_start:NE_end]
                chunk_tokens = tokenizer.tokenize(chunk_text)
                tokens += chunk_tokens
                ner_tags += [section_mentions.loc[i,'label']] * len(chunk_tokens)
                # print('NE', chunk_tokens)
                pos = NE_end
        
        # If there is not mention for this section:
        if len(section_mentions) == 0:
            final_start = 0
        else:
            # Final part:
            final_start = NE_end
            
        final_end = len(text)
        
        chunk_text = text[final_start:final_end]
        handle_none_NE_chunk(chunk_text, final_chunk=True)
    
    f.close()
