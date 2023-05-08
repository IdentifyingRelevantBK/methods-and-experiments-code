bottom_clauses(BCS) :- findall(FlatClause,(pos(E), sat(E), user:'$aleph_sat'(lastlit,Last),aleph:get_clause(1,Last,[],FlatClause,user)), BCS).

