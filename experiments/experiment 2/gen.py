
import random
import collections
import os
import random
import numpy as np

# zendo(A):- piece(A,B),red(B),blue(C),size(B,D),size(C,E),smaller(D,E),far(B,C).

DISTS_IN_BK = True

MAX_SIZE = 10
NUM_PIECES = 5
COLORS = ["blue", "red"]
N_TRIALS = 10
DIST_THRESHOLD = 0.4

NUM_TRAIN_POS = 50
NUM_TRAIN_NEG = 100
NUM_TEST_POS = 200
NUM_TEST_NEG = 200

INITIAL_BK = 'bk.pl'
INITIAL_BIAS = 'bias.pl'

DIST_BY_TASK = range(50, 501, 50)

def generate_zendo_problem(num_dists, output_dir):
    global DISTS
    global NUM_DISTS
    NUM_DISTS = num_dists
    DISTS = [f"dist{i}" for i in range(num_dists)]
   
    for trial in range(N_TRIALS):
        counter = 0
        pos_train_examples = gen_examples(counter, counter+NUM_TRAIN_POS, gen_pos)
        counter += NUM_TRAIN_POS
        neg_train_examples = gen_examples(counter, counter+NUM_TRAIN_NEG, gen_neg)
        counter += NUM_TRAIN_NEG
        pos_test_examples = gen_examples(counter, counter+NUM_TEST_POS, gen_pos)
        counter += NUM_TEST_POS
        neg_test_examples = gen_examples(counter, counter+NUM_TEST_NEG, gen_neg)
        counter += NUM_TEST_NEG
        
        write_task(os.path.join(output_dir, f"{trial}", "test"), INITIAL_BK, pos_test_examples, neg_test_examples)
        write_task(os.path.join(output_dir, f"{trial}", "train"), INITIAL_BK, pos_train_examples, neg_train_examples)
        
def write_task(output_dir, initial_bk, pos_examples, neg_examples):
    write_examples(output_dir, pos_examples, neg_examples)
    write_bk(output_dir, initial_bk, pos_examples, neg_examples)
    write_bias(output_dir)

def write_bias(output_dir):
    os.system(f"cp {INITIAL_BIAS} {output_dir}/bias.pl")

    with open(f"{output_dir}/bias.pl", "a") as f:
        for dist in DISTS:
            f.write(f"body_pred({dist},1).\n")
            f.write(f"type({dist},(dist,)).\n")
            f.write(f"direction({dist},(in,)).\n")

def write_examples(output_dir, pos_examples, neg_examples):
    exs_file = mkfile(output_dir, 'exs.pl')
    with open(exs_file, 'w+') as f:
        for w_id, _ in pos_examples:
            f.write(f'pos(zendo({w_id})).\n')
        for w_id, _ in neg_examples:
            f.write(f'neg(zendo({w_id})).\n')
    return exs_file

def write_bk(output_dir, initial_bk, pos_examples, neg_examples):
    bk = ":-style_check(-discontiguous).\n"
    bk += make_bk(initial_bk, pos_examples, neg_examples)

    bk_file = mkfile(output_dir, 'bk.pl')
    with open(bk_file, 'w+') as bk_f:
        bk_f.write(bk)
    return bk_file
    
def add_far(piece1, piece2):
    if far(piece1[3], piece2[3]):
        return ""
        #return f"far({piece1[0]}, {piece2[0]}).\n"
    else:
        return ""
        #return f"not_far({piece1[0]}, {piece2[0]}).\n"
        
        
def add_dist(piece1, piece2, dist):
    #return f"dist{dist}({piece1[0]}, {piece2[0]}).\n"
    return f"dist({piece1[0]}, {piece2[0]}, {dist}).\n"
        
def add_dists(pieces):
    n = len(pieces)
    M = np.zeros((n, n), np.int32)
    
    for i in range(n):
        for j in range(i):
            M[i][j] = M[j][i] = random.choice(range(NUM_DISTS))
            
    bk = ""
            
    for i in range(n):
        for j in range(n):
           bk += add_dist(pieces[i], pieces[j], M[i][j]) 
           
    return bk

def make_bk(initial_bk, pos_examples, neg_examples):
    with open(initial_bk, 'r') as initial_bk_f:
        bk = initial_bk_f.read()
        bk += "\n\n"

    for w_id, pieces in pos_examples:
        for piece in pieces:
            bk += bk_piece(w_id, piece)
     
        for piece1 in pieces:
            for piece2 in pieces:
                bk += add_far(piece1, piece2)
    
        bk += add_dists(pieces)
        
    
    for w_id, pieces in neg_examples:
        for piece in pieces:
            bk += bk_piece(w_id, piece)
        
        for piece1 in pieces:
            for piece2 in pieces:
                bk += add_far(piece1, piece2)
    
        bk += add_dists(pieces)
    
    for dist in DISTS:
        bk += f":- dynamic {dist}/1.\n"
    
    for i in range(len(DISTS)):
        bk += f"dist{i}({i}).\n"
    
    return bk

def bk_piece(w_id, piece):
    bk_piece = ""
    name, size, color, _ = piece
    bk_piece += f"piece({w_id}, {name}).\n"
    bk_piece += f"size({name}, {size}).\n"
    bk_piece += f"{color}({name}).\n"
    
    return bk_piece
        
def mkfile(base_path, rel_path):
    os.makedirs(base_path, exist_ok=True)
    p = os.sep.join([base_path, rel_path])
    return p
 
def gen_examples(i, j, fn):
    return [(k,fn(k)) for k in range(i, j)]
    
def gen_pos(w_id):
    pieces = gen_pieces(w_id)

    piece1 = pieces[0]
    piece2 = pieces[1]


    piece1[2] = "red"
    piece2[2] = "blue"
    
    if piece1[1] > piece2[1]:
        piece1[1], piece2[1] = piece2[1], piece1[1]


    assert is_positive(pieces)
    
    return pieces


def gen_neg(w_id):

    done = False
    
    while not done:
        pieces = gen_pieces(w_id)
            
        piece1 = pieces[0]
        piece2 = pieces[1]
        

        piece1[1] = random.randint(0, MAX_SIZE)
        piece1[2] = "red"
        piece2[1] = random.randint(0, MAX_SIZE)
        piece2[2] = "blue"
        
        if piece1[1] > piece2[1]:
            piece1[1], piece2[1] = piece2[1], piece1[1]
                
        x = random.random()
        
        if x < 0.2:
            piece1[2] = random.choice(COLORS)
        elif x < 0.4:
            piece2[2] = random.choice(COLORS)
        elif x < 0.6: 
            piece1[1], piece2[1] = piece2[1], piece1[1]
        else:
            piece1[1], piece2[1] = piece2[1], piece1[1]
       
        
        done = not is_positive(pieces)
    return pieces  

def small(x):
    return x <= MAX_SIZE//3

def big(x):
    return x > 2*MAX_SIZE//3
    
def not_far(x, y):
    return abs(x-y) < DIST_THRESHOLD

def far(x, y):
    return abs(x-y) >= DIST_THRESHOLD
    
def smaller(x, y):
    return x <= y
    
def is_positive(pieces):
    def first_clause(piece1, piece2):
        return smaller(piece1[1], piece2[1]) and piece1[2] == "red" and piece2[2] == "blue"
   
    for piece1 in pieces:
        for piece2 in pieces:
            if first_clause(piece1, piece2):
                return True
                
    return False        
    
    
def gen_pieces(w_id):
    return [gen_piece(w_id, i) for i in range(NUM_PIECES)]

def gen_piece(w_id, p_id):
    name = f"p{w_id}_{p_id}"
    size = gen_size()
    c = gen_color()
    x = gen_xcoord()
    return [name, size, c, x]

def gen_size():
    return random.randint(0, MAX_SIZE)
    
def gen_xcoord():
    return random.random()

def gen_color():
    return random.choice(COLORS)

def generate_all_tasks():
    start_task = 0
    end_task = len(DIST_BY_TASK)

    for test_id in range(start_task, end_task):
        print(f"generating task {test_id}")
        generate_zendo_problem(DIST_BY_TASK[test_id], f"task{test_id}")


generate_all_tasks()
