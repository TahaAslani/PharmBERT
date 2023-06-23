# PharmBERT
A domain-specific BERT model for drug labels.

Please refer to the PharmBERT paper for the model description:

https://doi.org/10.1093/bib/bbad226

The cased and uncased versions of PharmBERT can be downloaded from the Hugging Face page of Liang Lab:

https://huggingface.co/Lianglab/PharmBERT-cased/tree/main

https://huggingface.co/Lianglab/PharmBERT-uncased/tree/main



# Codes of the paper
To reproduce the results run the following codes:
## Download this repo
```
wget https://github.com/TahaAslani/PharmBERT/archive/refs/heads/main.zip
unzip main.zip
rm main.zip
cd PharmBERT-main/
```

## Install dependencies
We recommend creating a new conda environment 
```
conda create -n PharmBERT python=3.8.10 -y
conda activate PharmBERT
```
Alternatively, you can install Python 3.8.10 in a different way. For example
```
conda install python=3.8.10 -y
```

Install the rest of the dependencies:
```
bash 1-install-dependancies.sh
```

You also need Cuda installed on your machine. We used Cuda 11.1.

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

## Citation
Please cite as:
```
@article{PharmBERT,
    author = {ValizadehAslani, Taha and Shi, Yiwen and Ren, Ping and Wang, Jing and Zhang, Yi and Hu, Meng and Zhao, Liang and Liang, Hualou},
    title = "{PharmBERT: a domain-specific BERT model for drug labels}",
    journal = {Briefings in Bioinformatics},
    year = {2023},
    month = {06},
    issn = {1477-4054},
    doi = {10.1093/bib/bbad226},
    url = {https://doi.org/10.1093/bib/bbad226},
    note = {bbad226},
    eprint = {https://academic.oup.com/bib/advance-article-pdf/doi/10.1093/bib/bbad226/50603440/bbad226.pdf},
}
```
