# PharmBERT
A domain specific BERT model for drug labels.

The cased and und uncased versions of PharmBERT can be downloaded from Hugging Face:
```
https://huggingface.co/Lianglab
```
The cased model:
```
https://huggingface.co/Lianglab/PharmBERT-cased/tree/main
```
The uncased model:
```
https://huggingface.co/Lianglab/PharmBERT-uncased/tree/main
```

# Codes of the paper
To reproduce the results run the followong codes:
## Download this repo
```
wget https://github.com/TahaAslani/PharmBERT/archive/refs/heads/main.zip
unzip main.zip
rm main.zip
cd PharmBERT-main/
```

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
bash ADR.sh Lianglab/PharmBERT-cased adr_data/cased adr_res_cased
```

Run the pipeline with PharmBERT uncased
```
bash ADR.sh Lianglab/PharmBERT-uncased adr_data/uncased adr_res_uncased
```
