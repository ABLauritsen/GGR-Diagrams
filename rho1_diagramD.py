import numpy as np
import sympy
import itertools
import cmath
from sympy.combinatorics import Permutation


n = 5

k = [sympy.symbols('k%d' % i) for i in range(1,n+1)]
x = [sympy.symbols('x%d' % i) for i in range(1,n+1)]


set_pi_ini = [Permutation(p).list() for p in itertools.permutations(range(n))]

set_pi_dis = [
	[list(itertools.permutations(range(1))), list(itertools.permutations(range(1,5)))],
	[list(itertools.permutations(range(3))), list(itertools.permutations(range(3,5)))],
	[list(itertools.permutations([0,3,4])), list(itertools.permutations([1,2]))],
	]
# print(set_pi_dis)

disallowed = [[(i + j) for i in set_pi_dis[l][0] for j in set_pi_dis[l][1]] for l in range(2)] 
disallowed = disallowed + [[ (Permutation([i[0],1,2,i[1],i[2]])*Permutation([0,j[0],j[1]],size=5)) for i in set_pi_dis[2][0] for j in set_pi_dis[2][1] ]]

# for l in range(3):
# 	print(l)
# 	for pi in disallowed[l]:
# 		# perm = Permutation([0] + [a+1 for a in pi])
# 		# print(Permutation(pi).list())


# Turns to list-form
for l in range(3):
	for j in range(len(disallowed[l])):
		pi = disallowed[l][j]
		disallowed[l][j] = Permutation(pi).list()


set_pi = []
for pi in set_pi_ini:
	if all(pi not in disallowed[l] for l in range(3)):
		set_pi = set_pi + [pi]

# for j in range(3):
# 	print('set_pi_dis', set_pi_dis[j])

linked = set_pi
print(len(set_pi))
# for p in set_pi:
# 	perm = Permutation([0] + [a+1 for a in p])
# 	print(perm)


no_linked = len(linked)
copies = np.ones(no_linked)


def flip45(perm):
	q = Permutation(3,4)
	return q*perm*q

def flip23(perm):
	q = Permutation([0,2,1],size=5)
	return q*perm*q

# for p in set_pi:
# 	perm = Permutation(p)
# 	print(perm, '&', flip23(perm))

def list_dupliactes(perm):
	out = [perm]
	for p in out:
		out = out + [flip45(p)]
	for p in out:
		out = out + [flip23(p)]
	for p in out:
		out = out + [~p]
	return out


list_reduced = []
weights = []

for i in range(no_linked):
	perm = Permutation(linked[i])

	list_copies = [perm]
	for p in list_dupliactes(perm):
		if p not in list_copies:
			list_copies = list_copies + [p]

	if all(item not in list_reduced for item in list_copies):
		list_reduced = list_reduced + [perm]
		weights = weights + [len(list_copies)]



no_perm = len(list_reduced)

signs = np.zeros(no_perm,dtype=int)



for i in range(no_perm):
	perm = list_reduced[i]
	# print(perm)
	p = Permutation(perm)
	sigma = (-1)**(int(p.is_even)+1)
	# print(sigma)
	signs[i] = sigma



def exp(p):
	# out = 'exp(' + str(1j*(k[index] - k[p[index]])*x[index]) + ')'
	out = ' &  ' + sympy.latex(k[0] - k[p[0]])
	return out

def ghat_str1(p):
	return ' &  ' + sympy.latex(-k[p[2]] + k[2]) 

def ghat_str2(p):
	return ' &  ' + sympy.latex(-k[p[4]] + k[4]) 

def chi_str1(p):
	return ' &  ' + sympy.latex(k[1] - k[p[1]] + k[2] - k[p[2]]) + '=0'

def chi_str2(p):
	return ' &  ' + sympy.latex(k[3] - k[p[3]] + k[4] - k[p[4]]) + '=0'



print('\\hline \\pi & \\hat{g}(\\cdots) & \\hat{g}(\\cdots) & \\chi(\\cdots) & \\chi(\\cdots) & \\textnormal{weight} & \\exp(i(\\cdots)x_1)')

for ind_perm in range(no_perm):
	perm = list_reduced[ind_perm]
	p = perm.list()
	p_new = [0] + [a+1 for a in p]
	perm_new = Permutation(p_new)

	string_temp = '\\\\' + str(perm_new) + ghat_str1(p) + ghat_str2(p) + chi_str1(p) + chi_str2(p) + ' & ' + str(signs[ind_perm]*weights[ind_perm]) + exp(p)
	print(string_temp)



