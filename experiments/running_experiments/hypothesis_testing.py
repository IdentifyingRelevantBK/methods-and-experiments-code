
from pyswip import Prolog
import sys      
        
# test a solution, solution_file is a file containing the Prolog learned hypothesis
def test(solution_file, test_bk_file, test_exs_file):
    prolog = Prolog()
    prolog.consult(test_exs_file)
    prolog.consult(test_bk_file)
    prolog.consult('test.pl')
    prolog.consult(solution_file)
    res = list(prolog.query('do_test(TP,FN,TN,FP)'))[0]
    print(f"test TP: {res['TP']}  FN: {res['FN']}, TN: {res['TN']}, FP: {res['FP']}")
    print(f"accuracy: {accuracy(res['TP'], res['FN'], res['TN'], res['FP'])}")
    
    
def accuracy(tp, fn, tn, fp):
    return (tp + tn) / (tp+fn+tn+fp)


test(sys.argv[1], sys.argv[2], sys.argv[3])

