# PharmBERT
A domain specific BERT model for drug labels


## Install dependancies
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

## Perform the Finetuning for ADR
To finetine for the ARR task:

Download all files of the train data
https://osf.io/6h9q4/
and save it in OSF/train

Download all files of the test data
https://osf.io/n84w3/
and save it in OSF/test


Convert data to json format:
```
python prepare_ard_data.py -d OSF -m bert-base-cased -o json_tokens_cased
```
Run the pipeline
```
bash ADR.sh output/Model-128/checkpoint-200000 json_tokens_cased adr_res
```
