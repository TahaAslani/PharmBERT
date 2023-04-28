model_path=$1
data_path=$2
output_dir=$3

train_file=$data_path/train.json
validation_file=$data_path/test.json

per_device_train_batch_size=16
learning_rate=0.0001
max_length=128

mkdir $output_dir

for seed in 42 555 666 999 9999
do
mkdir mkdir "$output_dir/$seed"
python run_ner_ard.py \
  --model_name_or_path $model_path \
  --train_file $train_file \
  --validation_file $validation_file \
  --output_dir "$output_dir/$seed" \
  --per_device_train_batch_size $per_device_train_batch_size \
  --learning_rate $learning_rate \
  --max_length $max_length \
  --seed $seed
done

python get_f1.py $output_dir
