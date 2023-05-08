import random
import collections
import os
import numpy as np

# pharma(A):- atom(A,B),atom_o(B),atom_h(C),bondA(B,C).
# pharma(A):- atom(A,B),atom_c(B),atom_cl(C),bondB(B,C).

MAX_ATOMS = 6
N_TRIALS = 10
NUM_BONDS = 8

INITIAL_BIAS = './bias.pl'

NUM_TRAIN_POS = 20
NUM_TRAIN_NEG = 200
NUM_TEST_POS = 200
NUM_TEST_NEG = 200

INITIAL_BK = './bk.pl'

ATOM_TYPES = ['h', 'o', 'cl', 'c']
        
P1 = 0.5
P2 = 0.5

assert P1 + P2 == 1

num_bonds_by_task = range(0, 1001, 100)

def generate_pharma_problem(output_dir, num_bonds):
    for trial in range(N_TRIALS):
        global IREL_BONDS
        global ALL_BONDS
        IREL_BONDS = [f"bond{i}" for i in range(num_bonds)]
        ALL_BONDS = IREL_BONDS.copy()
        ALL_BONDS.append("bondA")
        ALL_BONDS.append("bondB")
        

        counter = 0
        pos_train_examples = gen_examples(counter, counter+NUM_TRAIN_POS, gen_pos)
        counter += NUM_TRAIN_POS
        neg_train_examples = gen_examples(counter, counter+NUM_TRAIN_NEG, gen_neg)
        counter += NUM_TRAIN_NEG
        pos_test_examples = gen_examples(counter, counter+NUM_TEST_POS, gen_pos)
        counter += NUM_TEST_POS
        neg_test_examples = gen_examples(counter, counter+NUM_TEST_NEG, gen_neg)
        counter += NUM_TEST_NEG

        write_task(os.path.join(output_dir, f"{trial}", "test"), pos_test_examples, neg_test_examples)
        write_task(os.path.join(output_dir, f"{trial}", "train"), pos_train_examples, neg_train_examples)
        
            
def write_task(output_dir, pos_examples, neg_examples):
    write_examples(output_dir, pos_examples, neg_examples)
    write_bk(output_dir, pos_examples, neg_examples)
    write_bias(output_dir)


def write_examples(output_dir, pos_examples, neg_examples):
    exs_file = mkfile(output_dir, 'exs.pl')
    with open(exs_file, 'w+') as f:
        for w_id, _, _ in pos_examples:
            f.write(f'pos(pharma({w_id})).\n')
        for w_id, _, _ in neg_examples:
            f.write(f'neg(pharma({w_id})).\n')
    return exs_file

def write_bias(output_dir):
    with open(INITIAL_BIAS, "r") as f_initial:
        initial_bias = f_initial.read()
        initial_bias += "\n\n"

    with open(output_dir + "/bias.pl", "w") as f:
        f.write(initial_bias)
        for bond in IREL_BONDS:
            f.write(f"body_pred({bond},2).\n")
            f.write(f"type({bond},(atom,atom)).\n")
            f.write(f"direction({bond},(in,in)).\n")

def write_bk(output_dir, pos_bk, neg_bk):
    bk_file = mkfile(output_dir, 'bk.pl')

    with open(bk_file, 'w') as f:
        f.write(":-style_check(-discontiguous).\n\n")
        f.write(mk_bk(pos_bk, neg_bk))


def make_bond(atom1, atom2, bond_pred):  
    if bond_pred == "":
        return ""
    else: 
        return f"{bond_pred}({atom1},{atom2}).\n"

def mk_bk(pos_ex, neg_ex):
    bk_str = ""
    for i, atoms, bond in pos_ex:
        for a, t in atoms:
            bk_str += f"atom({i},{a}).\n"
            bk_str += f"atom_{t}({a}).\n"
        for k, a1 in enumerate(atoms):
            for j, a2 in enumerate(atoms):
                bk_str += make_bond(a1[0], a2[0], bond[k][j])

    for i, atoms, bond in neg_ex:
        for a, t in atoms:
            bk_str += f"atom({i},{a}).\n"
            bk_str += f"atom_{t}({a}).\n"
        for k, a1 in enumerate(atoms):
            for j, a2 in enumerate(atoms):
                bk_str += make_bond(a1[0], a2[0], bond[k][j])

    for bond in IREL_BONDS:
        bk_str += f":- dynamic {bond}/2.\n"
        
    return bk_str
    
        
def mkfile(base_path, rel_path):
    os.makedirs(base_path, exist_ok=True)
    p = os.sep.join([base_path, rel_path])
    return p
            
 
def gen_examples(i, j, fn):
    return [fn(k) for k in range(i, j)]

    
def gen_pos(n):
    
    if random.random() < P1: 
        atoms, bonds, _, _ = generate_2_fixed_types(n, 'o', 'h', "bondA")
    else:
        atoms, bonds, _, _ = generate_2_fixed_types(n, 'c', 'cl', "bondB")
     
    assert is_pos(atoms, bonds)
    return n, atoms, bonds


def gen_neg(n):    
    done = False
    
    while not done:
        x = random.random()
        
        if x < P1: # make it close to first clause
            x = x/P1
            
            if x < 0.2: # generate random example
                atoms = generate_atoms(n)
                bonds = generate_bond()
            else:
                atoms, bonds, pos_o, pos_h = generate_2_fixed_types(n, 'o', 'h', "bondA")
                if x < 0.3:
                    bonds[pos_o][pos_h] = random.choice(ALL_BONDS)
                    bonds[pos_h][pos_o] = bonds[pos_o][pos_h]
                elif x < 0.5:
                    atoms[pos_o] = generate_atom(n, pos_o)
                elif x < 0.6:
                    atoms[pos_h] = generate_atom(n, pos_h)
                else:
                    atoms[pos_o] = generate_atom(n, pos_o)
                    atoms[pos_h] = generate_atom(n, pos_h)
        else:  # make it close to first clause
            x = (x - P1) / P2

            if x < 0.2:  # generate random example
                atoms = generate_atoms(n)
                bonds = generate_bond()
            else:
                atoms, bonds, pos_c, pos_cl = generate_2_fixed_types(n, 'c', 'cl', "bondB")

                if x < 0.3:
                    bonds[pos_c][pos_cl] = random.choice(ALL_BONDS)
                    bonds[pos_cl][pos_c] = bonds[pos_c][pos_cl]
                elif x < 0.5:
                    atoms[pos_c] = generate_atom(n, pos_c)
                elif x < 0.6:
                    atoms[pos_cl] = generate_atom(n, pos_cl)
                else:
                    atoms[pos_c] = generate_atom(n, pos_c)
                    atoms[pos_cl] = generate_atom(n, pos_cl)

        done = not is_pos(atoms, bonds)
    
    return n, atoms, bonds


def is_pos(atoms, bonds):
    for i in range(MAX_ATOMS):
        for j in range(MAX_ATOMS):
            assert bonds[i][j] == bonds[j][i]
            if ((atoms[i][1] == 'o' and atoms[j][1] == 'h') or (atoms[j][1] == 'o' and atoms[i][1] == 'h')) and \
                    bonds[i][j] == "bondA":
                return True
            if ((atoms[i][1] == 'c' and atoms[j][1] == 'cl') or (atoms[j][1] == 'cl' and atoms[i][1] == 'c')) and \
                    bonds[i][j] == "bondB":
                return True
    return False


def generate_2_fixed_types(n, type1, type2, bond):
    atoms = []
    pos1, pos2 = random.sample(range(MAX_ATOMS), 2)
    
    atoms = generate_atoms(n)
    bonds = generate_bond()
    
    atoms[pos1][1] = type1
    atoms[pos2][1] = type2
    
    bonds[pos1][pos2] = bond
    bonds[pos2][pos1] = bond
    
    return atoms, bonds, pos1, pos2


def generate_atoms(n):
    atoms = []
    for k in range(MAX_ATOMS):
        atoms.append(generate_atom(n, k))
    return atoms

def generate_atom(n, i):
    atom_type = random.choice(ATOM_TYPES)

    id = str('a') + str(n) + "_" + str(i)
    return [id, atom_type]

def generate_bond():
    bond = [["" for i in range(MAX_ATOMS)] for j in range(MAX_ATOMS)]
    
    for i in range(NUM_BONDS):
        x, y = random.sample(range(MAX_ATOMS), 2)
        bond[x][y] = bond[y][x] = random.choice(ALL_BONDS)
    
    return bond


for i in range(len(num_bonds_by_task)):
    print(f"generating pharma task {i}")
    generate_pharma_problem(f"task{i}", num_bonds_by_task[i])
