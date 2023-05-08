import sys
import re
import numpy as np
import pandas as pd

test = sys.argv[1]
num_trials = int(sys.argv[2])

num_programs = np.empty(num_trials, dtype = int)
learning_time = np.empty(num_trials, dtype = float)
testing_accuracy = np.empty(num_trials, dtype = float)
training_precision = np.empty(num_trials, dtype = float)
training_recall = np.empty(num_trials, dtype = float)

for trial in range(num_trials):
  with open(f"{test}/{trial}/output.txt") as f:
    data = f.read()

  num_programs[trial] = int(re.search(r'\d+', data[data.find("Num. programs: "):]).group())
  learning_time[trial] = float(re.search(r'\d+\.\d*', data[data.find("Total execution time: "):]).group())
  testing_accuracy[trial] = float(re.search(r'\d+\.\d*', data[data.find("accuracy: "):]).group())
  training_precision[trial] = float(re.search(r'\d+\.\d*', data[data.find("Precision:"):]).group()) # true positive / (true positive + false positive)
  training_recall[trial] = float(re.search(r'\d+\.\d*', data[data.find("Recall:"):]).group()) # true positives / (true positives + false negatives)
 

df = pd.DataFrame({ "num_programs": num_programs, "learning_time": learning_time, "testing_accuracy": testing_accuracy, "training_precision": training_precision, "training_recall": training_recall})

df.to_csv(f"{test}/results.csv")
