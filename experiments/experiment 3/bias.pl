max_vars(4).
max_body(6).

head_pred(pharma,1).
body_pred(bondA,2).
body_pred(bondB,2).
body_pred(atom,2).

body_pred(atom_h,1).
body_pred(atom_c,1).
body_pred(atom_cl,1).
body_pred(atom_o,1).


type(pharma,(state,)).
type(bondA,(atom,atom)).
type(bondB,(atom,atom)).
type(atom,(state,atom)).

type(atom_h,(atom,)).
type(atom_c,(atom,)).
type(atom_cl,(atom,)).
type(atom_o,(atom,)).

direction(pharma,(in,)).
direction(bondA,(in, out)).
direction(bondB,(in, out)).
direction(atom,(in, out)).

direction(atom_o,(in,)).
direction(atom_h,(in,)).
direction(atom_cl,(in,)).
direction(atom_c,(in,)).
