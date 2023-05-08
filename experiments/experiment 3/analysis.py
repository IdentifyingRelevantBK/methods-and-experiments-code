import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import matplotlib.ticker
num_irel = range(0, 901, 100)

# which methods to plot

baseline = True
union_all = True
union_few = True
intersect = False


num_tasks = len(num_irel)


def plot_accuracy():
    
    fig1, ax1 = plt.subplots()

    def plot_one(df, label, xpoints):
        accuracy = [df[i]["testing_accuracy"] for i in range(num_tasks)]
        accuracy_means = [data.mean() for data in accuracy]
        accuracy_std = [data.std() for data in accuracy]
        ax1.plot(xpoints, accuracy_means, label=label)

    if baseline:
        plot_one(df_baseline, label="baseline", xpoints = num_irel)
    
    if union_all:
        plot_one(df_union_all, label="BC-union-all", xpoints = num_irel)
   
    if union_few:
        plot_one(df_union_few, label="BC-union-few", xpoints = num_irel)
    
    if intersect:
        plot_one(df_intersect, label="BC-intersect", xpoints = num_irel)

    plt.grid(axis='y')

    ax1.set_xticks(num_irel)

    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.xlabel("# irrelevant predicates")
    plt.ylabel("accuracy")
    plt.legend()
    plt.title("Predictive accuracy")

    plt.savefig("accuracy.png")
    plt.clf()

color = {"baseline": "tab:blue", "BC-union-all": "tab:orange", "BC-union-few": "tab:green", "BC-intersect": "tab:red"}
linestyle = {"baseline": "solid", "BC-union-all": "solid", "BC-union-few": "solid", "BC-intersect": "dotted"}

def plot_number_programs():

    fig1, ax1 = plt.subplots()

    def plot_one(df, label, xpoints):
        num_programs = [df[i]["num_programs"] for i in range(num_tasks)]
        num_program_means = [data.mean() for data in num_programs]
        num_programs_std = [data.std() for data in num_programs]
        ax1.errorbar(xpoints, num_program_means, yerr=num_programs_std, label=label, color=color[label], linestyle=linestyle[label])

    if baseline:
        plot_one(df_baseline, label="baseline", xpoints = num_irel)
    
    if union_all:
        plot_one(df_union_all, label="BC-union-all", xpoints = num_irel)
   
    if union_few:
        plot_one(df_union_few, label="BC-union-few", xpoints = num_irel)
    
    if intersect:
        plot_one(df_intersect, label="BC-intersect", xpoints = num_irel)

    plt.grid(axis='y')

    ax1.set_xticks(num_irel)

    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.xlabel("# irrelevant predicates", fontsize=14)
    plt.ylabel("# searched programs", fontsize=14)

    plt.legend(fontsize=14)
    ax1.xaxis.set_tick_params(labelsize=14)
    ax1.yaxis.set_tick_params(labelsize=14)

    plt.title("Number of searched programs", fontsize=20)

    plt.savefig("num_searched_programs.png")
    plt.clf()


def plot_total_learning_time():

    fig1, ax1 = plt.subplots()

    def plot_one(df, label, column, xpoints):

        learning_time = [df[i][column] for i in range(num_tasks)]
        learning_time_means = [data.mean() for data in learning_time]
        learning_time_std = [data.std() for data in learning_time]
        ax1.errorbar(xpoints, learning_time_means, yerr=learning_time_std, label=label, marker='.', color=color[label], linestyle=linestyle[label])

    if baseline:
        plot_one(df_baseline, label="baseline", column="learning_time", xpoints = num_irel)
    
    if union_all:
        plot_one(df_union_all, label="BC-union-all", column="total_learning_time", xpoints = num_irel)
    
    if union_few:
        plot_one(df_union_few, label="BC-union-few", column="total_learning_time", xpoints = num_irel)    

    if intersect:
        plot_one(df_intersect, label="BC-intersect", column="total_learning_time", xpoints = num_irel)
    
    
    plt.grid(axis='y')

    ax1.set_xticks(num_irel)

    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    

    plt.legend(fontsize=14)
    ax1.xaxis.set_tick_params(labelsize=14)
    ax1.yaxis.set_tick_params(labelsize=14)


    plt.xlabel("# irrelevant predicates", fontsize=14)
    plt.ylabel("learning time(s)", fontsize=14)
    plt.title("Cumulative learning time", fontsize=20)

    plt.savefig("cumulative_learning_time.png")
    plt.clf()
    
   

def plot_learning_time_excluding_pruning():

    fig1, ax1 = plt.subplots()

    def plot_one(df, label, column, xpoints):

        learning_time = [df[i][column] for i in range(num_tasks)]
        learning_time_means = [data.mean() for data in learning_time]
        learning_time_std = [data.std() for data in learning_time]
        ax1.errorbar(xpoints, learning_time_means, yerr=learning_time_std, label=label, marker='.', color=color[label], linestyle=linestyle[label])

    if baseline:
        plot_one(df_baseline, label="baseline", column="learning_time", xpoints = [x for x in num_irel])
    
    if union_all:
        plot_one(df_union_all, label="BC-union-all", column="learning_time", xpoints = num_irel)
    
    if union_few:
        plot_one(df_union_few, label="BC-union-few", column="learning_time", xpoints = [x for x in num_irel])
    
    if intersect:
        plot_one(df_intersect, label="BC-intersect", column="learning_time", xpoints = [x for x in num_irel])
    

    plt.grid(axis='y')

    ax1.set_xticks(num_irel)

    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    

    plt.legend(fontsize=14)
    ax1.xaxis.set_tick_params(labelsize=14)
    ax1.yaxis.set_tick_params(labelsize=14)


    plt.xlabel("# irrelevant predicates", fontsize=14)
    plt.ylabel("learning time(s)", fontsize=14)
    plt.title("Learning time excluding pruning", fontsize=20)

    plt.savefig("learning_time_without_pruning.png")
    plt.clf()


def plot_bottom_clause_time():
    fig1, ax1 = plt.subplots()
    
    def plot_one(df, label, xpoints):
        bottom_clause_construction_times = [df[i]["time_bottom_clause_construction"] for i in range(num_tasks)]
        bottom_clause_construction_time_means = [data.mean() for data in bottom_clause_construction_times]
        bottom_clause_construction_time_std = [data.std() for data in bottom_clause_construction_times]  
        ax1.errorbar(num_irel, bottom_clause_construction_time_means, yerr=bottom_clause_construction_time_std, label=label, color=color[label], linestyle=linestyle[label])
    
    if union_all: 
        plot_one(df_union_all, label = "BC-union-all", xpoints = num_irel)
    
    if union_few:
        plot_one(df_union_few, label = "BC-union-few", xpoints = num_irel)
    
    if intersect:
        plot_one(df_intersect, label = "BC-intersect", xpoints = num_irel)
    
    
    ax1.set_xticks(num_irel)
    plt.grid(axis='y')
    
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    plt.xlabel("# irrelevant predicates", fontsize=14)
    plt.ylabel("pruning time(s)", fontsize=14)
    plt.title("Pruning time", fontsize=20)

    plt.legend(fontsize=14)
    ax1.xaxis.set_tick_params(labelsize=14)
    ax1.yaxis.set_tick_params(labelsize=14)


    plt.savefig("pruning_time.png")
    plt.clf()
    
    

def plot_removed_preds():
    fig1, ax1 = plt.subplots()
    
    def plot_one(df, label, xpoints):
        removed_preds = [df[i]["removed_preds"] for i in range(num_tasks)] 
        removed_preds_means = [data.mean() for data in removed_preds]
        removed_preds_std = [data.std() for data in removed_preds]
        ax1.errorbar(xpoints, removed_preds_means, yerr=removed_preds_std, label = label, color=color[label], linestyle=linestyle[label])
    
    if union_all:
        plot_one(df_union_all, label = "BC-union-all", xpoints = num_irel)
    
    if union_few:
        plot_one(df_union_few, label = "BC-union-few", xpoints = [x + 1 for x in num_irel])
    
    if intersect:
        plot_one(df_intersect, label = "BC-intersect", xpoints = [x + 1 for x in num_irel])
    
    plt.grid(axis='y')
    
    ax1.set_xticks(num_irel)
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    plt.xlabel("# irrelevant predicates")
    plt.ylabel("# removed predicates")
    plt.title("Number of removed predicates")
    plt.legend()

    plt.savefig("removed_preds.png")
    plt.clf()
    
    

def plot_removed_preds_percentage():
    fig1, ax1 = plt.subplots()
    
    def plot_one(df, label, xpoints):
        removed_preds = [df[i]["removed_preds"] / num_irel[i] * 100 for i in range(num_tasks)] 
        removed_preds_means = [data.mean() for data in removed_preds]
        removed_preds_std = [data.std() for data in removed_preds]
        ax1.errorbar(xpoints, removed_preds_means, yerr=removed_preds_std, label = label, color=color[label], linestyle=linestyle[label])
    
    if union_all:
        plot_one(df_union_all, label = "BC-union-all", xpoints = num_irel)
    
    if union_few:
        plot_one(df_union_few, label = "BC-union-few", xpoints = [x + 1 for x in num_irel])
    
    if intersect:
        plot_one(df_intersect, label = "BC-intersect", xpoints = [x + 1 for x in num_irel])
    
    plt.grid(axis='y')
    
    ax1.set_xticks(num_irel)
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    plt.xlabel("# irrelevant predicates", fontsize=14)
    plt.ylabel("irrelevant predicates removed (%)", fontsize=14)
    plt.title("Irrelevant predicates removed (%)", fontsize=20)

    plt.legend(fontsize=14)
    ax1.xaxis.set_tick_params(labelsize=14)
    ax1.yaxis.set_tick_params(labelsize=14)


    plt.savefig("removed_preds_percentage.png")
    plt.clf()


name_union_all = "union_all"
name_baseline = "baseline"
name_union_few = "union_few"
name_intersect = "intersect"

for i in range(num_tasks):
    # parse the output of the pruning method to get the running time
    
    if union_all:
        os.system(f"python3 ../{name_union_all}/parse_bottom_clause_info.py ../{name_union_all}/task{i} 10")
    
    if union_few:
        os.system(f"python3 ../{name_union_few}/parse_bottom_clause_info.py ../{name_union_few}/task{i} 10")
        
    if intersect:
        os.system(f"python3 ../{name_intersect}/parse_bottom_clause_info.py ../{name_intersect}/task{i} 10")

if union_all:
    df_union_all = [pd.read_csv(f"../{name_union_all}/task{i}/results.csv") for i in range(num_tasks)]

if baseline:
    df_baseline = [pd.read_csv(f"../{name_baseline}/task{i}/results.csv") for i in range(num_tasks)]

if union_few:
    df_union_few = [pd.read_csv(f"../{name_union_few}/task{i}/results.csv") for i in range(num_tasks)]


if intersect:
    df_intersect = [pd.read_csv(f"../{name_intersect}/task{i}/results.csv") for i in range(num_tasks)]


for i in range(num_tasks): 
    
    if union_all:
        df_union_all[i]["total_learning_time"] = df_union_all[i]["learning_time"] + df_union_all[i]["time_bottom_clause_construction"]
        df_union_all[i].to_csv(f"../{name_union_all}/task{i}/results.csv")
    
    if union_few:    
        df_union_few[i]["total_learning_time"] = df_union_few[i]["learning_time"] + df_union_few[i]["time_bottom_clause_construction"]
        df_union_few[i].to_csv(f"../{name_union_few}/task{i}/results.csv")
    
    if intersect:    
        df_intersect[i]["total_learning_time"] = df_intersect[i]["learning_time"] + df_intersect[i]["time_bottom_clause_construction"]
        df_intersect[i].to_csv(f"../{name_intersect}/task{i}/results.csv")


plot_number_programs()
plot_total_learning_time()
plot_bottom_clause_time()
plot_removed_preds()
plot_removed_preds_percentage()
plot_learning_time_excluding_pruning()
plot_accuracy()
