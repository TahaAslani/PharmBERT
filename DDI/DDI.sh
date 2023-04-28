data_path=/ifs/groups/liangGrp/tv349/PharmaBERT/DDI/Eval2013/data/TSV
init_model_path=/ifs/groups/liangGrp/tv349/PharmaBERT/HuggingFace/bert-base-cased/Model-128/checkpoint-200000
res_path=res


for seed in 123 1234 100 1000 22
do

  mkdir -p $res_path/$seed

  #python /home/tv349/PharmaBERT/DDI/Eval2013/DESC_MOL-DDIE-master/main/run_bert_only_taha.py \
  python run_bert_only_taha.py \
    --task_name MRPC \
    --model_type bert \
    --data_dir $data_path \
    --model_name_or_path $init_model_path \
    --output_dir $res_path/$seed \
    --max_seq_length 128 \
    --per_gpu_train_batch_size 32 \
    --num_train_epochs 3 \
    --do_train \
    --do_eval \
    --seed $seed \
    --fp16

done

python Eval.py $res_path
