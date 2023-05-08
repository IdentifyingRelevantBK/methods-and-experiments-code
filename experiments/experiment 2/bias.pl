
max_vars(5).
max_body(8).

head_pred(zendo,1).
body_pred(piece,2).

body_pred(size,2).
body_pred(blue,1).
body_pred(red,1).




body_pred(smaller,2).

type(zendo,(state,)).
type(piece,(state,piece)).

type(size,(piece,real)).
type(blue,(piece,)).
type(red,(piece,)).






type(smaller,(real,real)).

direction(zendo,(in,)).
direction(piece,(in,out)).

direction(size,(in,out)).
direction(blue,(in,)).
direction(red,(in,)).




direction(smaller,(in,in)).

body_pred(dist,3).
type(dist,(piece,piece,dist)).
direction(dist,(in,in,out)).


