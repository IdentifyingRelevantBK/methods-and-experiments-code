
max_vars(5).
max_body(6).

head_pred(zendo,1).
body_pred(piece,2).
body_pred(not_far,2).
body_pred(blue,1).
body_pred(red,1).

type(zendo,(state,)).
type(piece,(state,piece)).
type(blue,(piece,)).
type(red,(piece,)).
type(not_far,(piece,piece)).

direction(zendo,(in,)).
direction(piece,(in,out)).
direction(not_far,(in,out)).
direction(blue,(in,)).
direction(red,(in,)).

