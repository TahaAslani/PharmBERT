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


To finetine for the ARD task:
Cased:
```
ARD.sh cased 'json_tokens_cased'
```

Uncased:
```
ARD.sh uncased 'json_tokens_uncased'
```
