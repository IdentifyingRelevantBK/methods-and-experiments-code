# $1 is the task
# $2 is the number of trials

task=$1
num_trials=$2

for (( trial=0; trial < $num_trials; trial++ ))
do
  ./run_single_trial.sh $task $trial
done

python3 parse_output.py $task $num_trials