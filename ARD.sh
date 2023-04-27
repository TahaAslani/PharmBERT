data_path=$2
train_file=$data_path/train.json
validation_file=$data_path/test.json

per_device_train_batch_size=16
learning_rate=0.0001
max_length=128


# Select the model to train
if [[ $1 == "cased" ]]; then
     model_path='bert-base-cased'
elif [[ $1 == "uncased" ]]; then
     model_path='bert-base-uncased'
else 
     echo "Either select cased or uncased model!"
     exit $exit_code
fi

output_dir='ARD-'$1


mkdir $output_dir

for seed in 42 555 666 999 9999
do
mkdir $output_dir\$seed
python transformers-4.14.1-release/examples/pytorch/token-classification/run_ner_no_trainer.py \
  --model_name_or_path $model_path \
  --train_file $train_file \
  --validation_file $validation_file \
  --output_dir $output_dir\$seed \
  --per_device_train_batch_size $per_device_train_batch_size \
  --learning_rate $learning_rate \
  --max_length $max_length \
  --seed $seed
done

python get_f1.py $output_dir
