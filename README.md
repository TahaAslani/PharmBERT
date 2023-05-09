# PharmBERT
A domain specific BERT model for drug labels


## Install dependancies
We recommend creating a new conda enviroenmet 
```
conda create -n PharmBERT python=3.8.10 -y
conda activate PharmBERT
```
Alternatively, you can install python 3.8.10 in a different way. For example
```
conda install python=3.8.10 -y
```

Install the rest of the dependancies:
```
bash 1-install-dependancies.sh
```

You also need a function Cuda installed on your machine. We used cuda 11.1.

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

Run the pipeline with PharmBERT cased
```
bash ADR.sh output/Model-128/checkpoint-200000 adr_data/cased adr_res_cased
```

Run the pipeline with PharmBERT uncased
```
bash ADR.sh output/Model-128/checkpoint-200000 adr_data/uncased adr_res_uncased
```
