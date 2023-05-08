import sys
import random
import collections
import os

# zendo(A):- piece(A,C),blue(C),contact(C,D),red(D).

# Irrelevant predicates are of the form shape_i(piece)


MAX_SIZE = 10
NUM_PIECES = 5
COLORS = ["blue", "red"]
THRESHOLD = 1
N_TRIALS = 10
NUM_TRAIN_POS = 20
NUM_TRAIN_NEG = 200
NUM_TEST_POS = 200
NUM_TEST_NEG = 200
DIST_THRESHOLD = 0.2

ALLOW_SHAPES = True

# these two contain some initial bias and BK, common to all tasks
INITIAL_BK = 'bk_init.pl'
INITIAL_BIAS = 'bias_init.pl'

BIAS = 'bias.pl'  # name of the original bias file, before applying our method to filter it
SHAPES_BY_TASK = range(500, 5001, 500)


def generate_zendo_problem(num_shapes, output_dir):
    global SHAPES

    SHAPES = [f"shape{i}" for i in range(num_shapes)]

    for trial in range(N_TRIALS):
        counter = 0
        pos_train_examples = gen_examples(counter, counter + NUM_TRAIN_POS, gen_pos)
        counter += NUM_TRAIN_POS
        neg_train_examples = gen_examples(counter, counter + NUM_TRAIN_NEG, gen_neg)
        counter += NUM_TRAIN_NEG
        pos_test_examples = gen_examples(counter, counter + NUM_TEST_POS, gen_pos)
        counter += NUM_TEST_POS
        neg_test_examples = gen_examples(counter, counter + NUM_TEST_NEG, gen_neg)
        counter += NUM_TEST_NEG

        write_task(os.path.join(output_dir, f"{trial}", "test"), INITIAL_BK, pos_test_examples, neg_test_examples)
        write_task(os.path.join(output_dir, f"{trial}", "train"), INITIAL_BK, pos_train_examples, neg_train_examples)


def write_task(output_dir, initial_bk, pos_examples, neg_examples):
    write_examples(output_dir, pos_examples, neg_examples)
    write_bk(output_dir, initial_bk, pos_examples, neg_examples)
    write_bias(output_dir)


def write_bias(output_dir):
    os.system(f"cp {INITIAL_BIAS} {output_dir}/{BIAS}")

    with open(f"{output_dir}/{BIAS}", "a") as f:
        for shape in SHAPES:
            f.write(f"body_pred({shape},1).\n")
            f.write(f"type({shape},(piece,)).\n")
            f.write(f"direction({shape},(in,)).\n")


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
    bk += ":- dynamic contact/2.\n"
    bk += make_bk(initial_bk, pos_examples, neg_examples)

    bk_file = mkfile(output_dir, 'bk.pl')
    with open(bk_file, 'w+') as bk_f:
        bk_f.write(bk)
    return bk_file


def make_bk(initial_bk, pos_examples, neg_examples):
    with open(initial_bk, 'r') as initial_bk_f:
        bk = initial_bk_f.read()
        bk += "\n\n"

    for w_id, pieces in pos_examples:
        for piece in pieces:
            bk += bk_piece(w_id, piece)
        
        for piece1 in pieces:
            for piece2 in pieces:
                if not_far(piece1[2], piece2[2]):
                    bk += f"not_far({piece1[0]}, {piece2[0]}).\n"         

            
    for w_id, pieces in neg_examples:
        for piece in pieces:
            bk += bk_piece(w_id, piece)
        
        for piece1 in pieces:
            for piece2 in pieces:
                if not_far(piece1[2], piece2[2]):
                    bk += f"not_far({piece1[0]}, {piece2[0]}).\n"         
                
    for shape in SHAPES:
        bk += f":- dynamic {shape}/1.\n"

    return bk


def bk_piece(w_id, piece):
    bk_piece = ""
    name, color, _ = piece
    bk_piece += f"piece({w_id}, {name}).\n"
    bk_piece += f"{color}({name}).\n"
    
    if ALLOW_SHAPES:
        shape = gen_shape()
        bk_piece += f"{shape}({name}).\n"
    
    return bk_piece        


def mkfile(base_path, rel_path):
    os.makedirs(base_path, exist_ok=True)
    p = os.sep.join([base_path, rel_path])
    return p


def gen_examples(i, j, fn):
    return [(k,fn(k)) for k in range(i, j)]


def gen_pieces(w_id):
    return [gen_piece(w_id, i) for i in range(NUM_PIECES)]

def gen_pos(w_id):
    pieces = gen_pieces(w_id)
    
    piece1 = pieces[0]
    piece2 = pieces[1]
    
    piece1[1] = "red"
    piece2[1] = "blue"
    
    while not not_far(piece1[2], piece2[2]):
        piece1[2] = gen_xcoord()    
        piece2[2] = gen_xcoord()
    
    assert is_positive(pieces)
    return pieces


def gen_neg(w_id):
    done = False
    
    while not done:    
        pieces = gen_pos(w_id)
        x = random.random()
    
        if x < 0.25:
            pieces[0][1] = "blue"
        elif x < 0.5:
            pieces[1][1] = "red"
        else:
            while not_far(pieces[0][2], pieces[1][2]):
                pieces[0][2] = gen_xcoord()    
                pieces[1][2] = gen_xcoord()
        
        done = not is_positive(pieces)     
     
    assert not is_positive(pieces)
    return pieces
            
def is_positive(pieces):
    for piece1 in pieces:
        for piece2 in pieces:
            if piece1[1] == "red" and piece2[1] == "blue" and not_far(piece1[2], piece2[2]):
                return True
    return False

def gen_piece(w_id, p_id):
    name = f"p{w_id}_{p_id}"
    c = gen_color()
    x = gen_xcoord()

    return [name, c, x]


def gen_xcoord():
    return random.random()

def not_far(x, y):
    return abs(x-y) < DIST_THRESHOLD

def gen_size():
    return random.randint(0, MAX_SIZE)
    
def gen_shape():
    return random.choice(SHAPES)

def gen_color():
    return random.choice(COLORS)

def generate_all_tasks():
    for test_id in range(len(SHAPES_BY_TASK)):
        print(f"generating task {test_id}")
        generate_zendo_problem(SHAPES_BY_TASK[test_id], f"task{test_id}")


generate_all_tasks()
