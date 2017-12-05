from __future__ import print_function

import sys

import cplex
from cplex.exceptions import CplexError
# F =ψsocial + ψfact +
# Xn
# i=1
# Xn
# j=1
# ψ

alpha_r, alpha_badr, alpha_itself, alpha_faction, alpha_bl, alpha_badbl = (0.7, -0.8, 0.4, 0.5, 0.1, -0.5)


#  For computational
# efficiency and to avoid erroneous propagation,
# soft constraints associated with reciprocity
# and balance theory are introduced only on pairs
# for which a high-precision classifier assigned polarity.

F = cplex.Cplex()

# get all pos_i,j first
F.objective.set_sense(F.objective.sense.maximize)

######## pair wise weights ########
my_lin   = []
my_rhs   = []
my_sense = []
names = []
n =3 # no_of_entities


#ψ_fact = faction inference
for i in range(1, n):
	for j in range(1,n):
		F.variables.add(obj=[alpha_itself], names=['itself'+str(i)+'_'+str(j)],types='B')
		for k in range(1, n):
			F.variables.add(obj=[alpha_faction]     , names=['tie_same'+str(i)+'_'+str(j)+'_'+str(k)],types='B')
			F.variables.add(obj=[alpha_faction * -1], names=['tie_diff'+str(i)+'_'+str(j)+'_'+str(k)],types='B')

#ψ_r = reciprocitiy constraint
for i in range(1, n+1):
	for j in range(1,n+1):
		F.variables.add(obj=[alpha_r], names=['r_same'+str(i)+'_'+str(j)],types='B')
		F.variables.add(obj=[alpha_badr], names=['r_diff'+str(i)+'_'+str(j)],types='B')

#ψ_bl = balance theory
for i in range(1, n+1):
	for j in range(1,n+1):
		for k in range(1, n+1):
			F.variables.add(obj=[alpha_bl], names=['pos_name'+str(i)+'_'+str(j)+'_'+str(k)],types='B')
			F.variables.add(obj=[alpha_bl], names=['neg_diff'+str(i)+'_'+str(j)+'_'+str(k)],types='B')
			F.variables.add(obj=[alpha_badbl], names=['pos_diff'+str(i)+'_'+str(j)+'_'+str(k)],types='B')
			F.variables.add(obj=[alpha_badbl], names=['neg_name'+str(i)+'_'+str(j)+'_'+str(k)],types='B')

for i in range(1, n+1):
	for j in range(1, n+1):
		F.variables.add(obj=[0.4], names=['pos'+str(i)+'_'+str(j)],types='B')
		my_lin.append(cplex.SparsePair(ind=['pos'+str(i)+'_'+str(j)], val=[1]))
		F.variables.add(obj=[0.4], names=['neg'+str(i)+'_'+str(j)],lb=[0], ub=[1],types='B')
		my_lin.append(cplex.SparsePair(ind=['neg'+str(i)+'_'+str(j)], val=[1]))
		F.variables.add(obj=[0.2], names=['neu'+str(i)+'_'+str(j)],lb=[0], ub=[1],types='B')
		my_lin.append(cplex.SparsePair(ind=['neu'+str(i)+'_'+str(j)], val=[1]))
		my_sense.append('E')
		my_rhs.append(1)
		names.append(['pair'+str(i)+'_'+str(j)])
		#print (my_lin, my_rhs)
F.write('example.lp')
#F.linear_constraints.add(names = names, lin_expr= my_lin, rhs=my_rhs, senses=my_sense)


try:
	F.solve()
except CplexError as exc:
    print(exc)

