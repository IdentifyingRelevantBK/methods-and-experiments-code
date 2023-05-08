import sys
import re
import numpy as np
import pandas as pd

task = sys.argv[1]
num_trials = int(sys.argv[2])

df = pd.read_csv(f"{task}/results.csv")

time_bottom_clause_construction = np.zeros(num_trials, dtype = float)
removed_preds = np.zeros(num_trials, dtype = int)


for trial in range(num_trials):
  with open(f"{task}/{trial}/bottom_clause.txt") as f:
    data = f.read()
    
  time_bottom_clause_construction[trial] = float(re.findall(r'Total time: (.*)\n', data)[0])
  removed_preds[trial] = int(re.findall(r'Removed (.*) predicates\n', data)[0])

df["time_bottom_clause_construction"] = time_bottom_clause_construction
df["removed_preds"] = removed_preds

df.to_csv(f"{task}/results.csv")
