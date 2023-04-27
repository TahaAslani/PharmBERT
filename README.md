# PharmBERT
A domain specific BERT model for drug labels


## Install dependancies
```
bash 1-install-dependancies.sh
```

## Perform the domain-specific pre-training
To pretrain the uncased model:
```
pretrain.sh uncased
```

To pretrain the cased model:
```
pretrain.sh cased
```

## Perform the Finetuning for ARD
To finetine for the ARD task:

Prepare the data:
Download the train data
https://osf.io/6h9q4/
and save it in OSF/train

Download the test data
https://osf.io/n84w3/
and save it in OSF/test

```
prepare_ard_data.py -d OSF -m bert-base-cased -o json_tokens_cased
```
Run
```
ARD.sh cased json_tokens_cased
```


Uncased:
Prepare the data
```
prepare_ard_data.py -d ard_data -m bert-base-uncased -o json_tokens_uncased
```
Run

```
ARD.sh uncased json_tokens_uncased
```
