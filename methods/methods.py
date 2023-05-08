from pyswip import Prolog
import sys
import re
import time
from bias_file_parser import BiasFileParser
import random
import argparse
from itertools import takewhile


# Query all the examples at once
def get_bottom_clauses(bk_file, aleph_bias_file, examples): 
    with open(aleph_bias_file, "a") as f:
        f.write(examples)
    
    prolog = Prolog() 
    prolog.consult(bk_file) 
    prolog.consult(aleph_bias_file) 
    prolog.consult("BCS.pl")
    
    res = list(prolog.query(f'bottom_clauses(BCS)'))[0]['BCS']
    erase_args = lambda pred: pred.split('(')[0]
    res = [list(map(erase_args, r)) for r in res]
       
    return res

def get_intersection(bottom_clauses): 
    inter = set(bottom_clauses[0])
  
    for bcl in bottom_clauses:
        inter = inter.intersection(bcl)

    return inter

def get_union(bottom_clauses):
    uni = set()

    for bcl in bottom_clauses:
        uni = uni.union(bcl)
    return uni    
    

def BC_intersect():
    if args.K:
        positive_examples_used = random.sample(positive_examples, args.K)
    else:
        positive_examples_used = positive_examples
    
    examples_query = "".join([f"pos({e}).\n" for e in positive_examples_used])
    bottom_clauses = get_bottom_clauses(args.bk_file, args.bias_file_aleph, examples_query)
    return get_intersection(bottom_clauses)


def BC_union_all():
    examples_query = "".join([f"pos({e}).\n" for e in positive_examples])
    bottom_clauses = get_bottom_clauses(args.bk_file, args.bias_file_aleph, examples_query)
    return get_union(bottom_clauses)


def BC_union_few():
    if not args.K:
        args.K = 10
 
    positive_examples_subset = random.sample(positive_examples, args.K)
    examples_query = "".join([f"pos({e}).\n" for e in positive_examples_subset])
    bottom_clauses = get_bottom_clauses(args.bk_file, args.bias_file_aleph, examples_query)
    return get_union(bottom_clauses)    


def BC_freq():
    if not args.W:
        args.W = 50 # select predicates that appear at least W times
 
    ordered_preds = BC_freq_order()

    return [p[0] for p in takewhile(lambda p: p[1] >= args.W, ordered_preds)]

# Return the predicates sorted in decreasing order of frequency in the bottom clauses
def BC_freq_order():
    examples_query = "".join([f"pos({e}).\n" for e in positive_examples])
    bottom_clauses = get_bottom_clauses(args.bk_file, args.bias_file_aleph, examples_query)
    
    dict = {} 
    
    for bottom_clause in bottom_clauses:
        for pred in bottom_clause:
            dict[pred] = dict.get(pred, 0) + 1

    preds = [(pred, dict[pred]) for pred in dict.keys()] 

    # Sort by frequencies
    def sort_by_freq(pair):
        return pair[1] 

    preds.sort(key=sort_by_freq, reverse=True)
    
    return preds

# Delegate the correct pruning method, which returns a new bias
def select_relevant_preds(method):
    if method == "BC-intersect":
        return BC_intersect()
    elif method == "BC-union-all": 
        return BC_union_all()
    elif method == "BC-union-few":
        return BC_union_few()
    elif method == "BC-freq":
        return BC_freq()
    else:
        assert False, "method not supported yet"

# Delegate the correct ordering method
def order_preds(method):
    if method == "BC-freq-order":
        return BC_freq_order()
    else:
        assert False, "method not supported yet"

# Returns true if the method produces an ordering of predicates
# And false if it produces a new language bias
def ordering_method(method):
    return method == "BC-freq-order"

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=True, choices=["BC-union-all", "BC-union-few", "BC-freq", "BC-freq-order", "BC-intersect"])
parser.add_argument('--bk-file', type=str, required=True)
parser.add_argument('--bias-file-popper', type=str, required=True)
parser.add_argument('--bias-file-aleph', type=str, required=True)
parser.add_argument('--bias-file-new', type=str, required=True)
parser.add_argument('--examples-file', type=str, required=True)
parser.add_argument('--frequencies-file', type=str)
parser.add_argument('--K', type=int)
parser.add_argument('--W', type=int)
args = parser.parse_args()

with open(args.examples_file, "r") as f:
    examples_data = f.read()

positive_examples = re.findall(r'pos\((.*)\)', examples_data)
bias_file_parser = BiasFileParser(args.bias_file_popper, args.bias_file_aleph, args.bias_file_new, args.bk_file)
bias_file_parser.translate_bias_file()

if ordering_method(args.method):
    ordered_preds = order_preds(args.method)
    assert args.frequencies_file != None
    
    with open(args.frequencies_file, "w") as f:
        for (pred, freq) in ordered_preds:
            f.write(f"{pred} appears {freq} times.\n")    
    print(f"Ordered {len(ordered_preds)} predicates")
else:
    relevant_preds = select_relevant_preds(args.method)
    print(relevant_preds)
    bias_file_parser.write_new_bias(relevant_preds)
    print(f"Removed {len(bias_file_parser.body_pred_dict.keys()) + len(bias_file_parser.head_pred_dict.keys()) - len(relevant_preds)} predicates")
    
finish_time = time.time()

print(f"Total time: {finish_time - start_time}")
