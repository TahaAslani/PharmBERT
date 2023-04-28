# File paths:
dailymed_url='https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/'
dailymed_spl_path='dailymed_spl.csv'
dailymed_spl_unique_path='dailymed_spl_unique.csv'
train_data_path='Unique.txt'
root_output_folder='output'


# Set training parameters:
max_seq_length=128
max_steps=200000
save_steps=20000
learning_rate=2e-5
batch_size=128

# Set the random seed
seed=42

# Select the model to train
if [[ $1 == "cased" ]]; then
     initial_model='bert-base-cased'
elif [[ $1 == "uncased" ]]; then
     initial_model='bert-base-uncased'
else 
     echo "Either select cased or uncased model!"
     exit $exit_code
fi

echo "Download and unzip DailyMed Data"
wget https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_zip_files_meta_data.zip
unzip dm_spl_zip_files_meta_data.zip

echo "Process DailyMed data"
python 2-dailymed_data.py -s $dailymed_spl_path -u $dailymed_url

echo "Remove duplicates"
python 3-remove_duplicate.py -i $dailymed_spl_path -o $dailymed_spl_unique_path

echo "Conver data to text"
python 4-convert-df-to-text.py -i $dailymed_spl_unique_path -o $train_data_path


echo "Create output directory"
output_path=$root_output_folder'/Model-128'
catch_path=$root_output_folder'/Catch-128'

mkdir $root_output_folder
mkdir $output_path
mkdir $catch_path

# Save limit
save_total_limit=$(($max_steps / $save_steps))

echo "Train the model"
python transformers-4.14.1-release/examples/pytorch/language-modeling/run_mlm.py \
  --train_file $train_data_path \
  --output_dir $output_path \
  --model_name_or_path $initial_model \
  --cache_dir $catch_path \
  --overwrite_cache True \
  --max_seq_length $max_seq_length \
  --do_train \
  --line_by_line True \
  --learning_rate $learning_rate \
  --max_steps $max_steps \
  --save_total_limit $save_total_limit \
  --save_steps $save_steps \
  --per_gpu_train_batch_size $batch_size \
  --seed $seed \
  
  echo "Done!"
