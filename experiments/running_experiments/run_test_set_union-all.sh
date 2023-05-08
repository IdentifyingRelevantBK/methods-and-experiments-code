# $1 is the test set name
# $2 is the number of tasks
# $3 is the number of trials in each task
# $4 is the first task to be run (default 0)

test_set=$1
num_tasks=$2
num_trials=$3

if [ -z "$4" ]
  then
    start_task=0
  else
    start_task=$4
fi

for (( task=start_task; task < $num_tasks; task++ ))
do
  ./run_task_union_all.sh $test_set/task$task $num_trials
done
