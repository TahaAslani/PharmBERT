# PharmBERT
A domain specific BERT model for drug labels


## Install dependancies
```
bash 1-install-dependancies.sh
```

## Perform the domain-specific pre-training
To pretrain the uncased model:
```
bash pretrain.sh uncased
```

To pretrain the cased model:
```
bash pretrain.sh cased
```

## Perform the Finetuning for ARD
To finetine for the ARD task:

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
bash ARD.sh cased json_tokens_cased
```
