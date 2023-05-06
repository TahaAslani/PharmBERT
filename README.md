# PharmBERT
A domain specific BERT model for drug labels


## Install dependancies
We recommend creating a new conda enviroenmet 
```
conda create -n PharmEBRT python=3.8.10 -y
source activate PharmEBRT
```

Install the rest of the dependancies
```
bash 1-install-dependancies.sh
```

You also need a function Cuda installed on your machine. We used cuda11.1.

## Perform the domain-specific pre-training
To pretrain the uncased model:
```
bash pretrain.sh uncased
```

To pretrain the cased model:
```
bash pretrain.sh cased
```

## Perform Finetuning for ADR
To finetine for the ARR task:

Download all files of the train data
https://osf.io/6h9q4/
and save it in adr_data/train

Download all files of the test data
https://osf.io/n84w3/
and save it in adr_data/test


Convert data to json format:
```
python prepare_ard_data.py -d adr_data -m bert-base-cased -o json_tokens_cased
```

Run the pipeline
```
bash ADR.sh output/Model-128/checkpoint-200000 json_tokens_cased adr_res
```
