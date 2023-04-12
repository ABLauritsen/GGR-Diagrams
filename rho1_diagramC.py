import numpy as np
import sympy
import itertools
import cmath
from sympy.combinatorics import Permutation


n = 4

k = [sympy.symbols('k%d' % i) for i in range(1,n+1)]
x = [sympy.symbols('x%d' % i) for i in range(1,n+1)]


set_pi_ini = list(itertools.permutations(range(4)))

set_pi_dis = [list(itertools.permutations(range(2))), list(itertools.permutations(range(2,4)))]
print(set_pi_dis)

disallowed = [ (i + j) for i in set_pi_dis[0] for j in set_pi_dis[1]]

set_pi = []
for pi in set_pi_ini:
	if pi not in disallowed:
		set_pi = set_pi + [pi]


linked = set_pi
# print(len(set_pi))
# for p in set_pi:
# 	print(Permutation(p))


no_linked = len(linked)
copies = np.ones(no_linked)


def flip34(perm):
	q = Permutation(2,3)
	return q*perm*q

for p in set_pi:
	perm = Permutation(p)
	print(perm, flip34(perm))

def list_dupliactes(perm):
	out = [perm]
	for p in out:
		out = out + [flip34(p)]
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
	out = ' &  ' + sympy.latex(k[0] - k[p[0]] + k[1]-k[p[1]])
	return out

def ghat_str1(p):
	return ' &  ' + sympy.latex(-k[p[1]] + k[1]) 

def ghat_str2(p):
	return ' &  ' + sympy.latex(-k[p[3]] + k[3]) 

def chi_str(p):
	return ' &  ' + sympy.latex(k[2] - k[p[2]] + k[3] - k[p[3]])  + '=0'





print('\\hline \\pi & \\hat{g}(\\cdots) & \\hat{g}(\\cdots) & \\chi(\\cdots) & \\textnormal{weight} & \\exp(i(\\cdots)x_1)')

for ind_perm in range(no_perm):
	perm = list_reduced[ind_perm]
	p = perm.list()
	p_new = [0] + [a+1 for a in p]
	perm_new = Permutation(p_new)

	string_temp = '\\\\' + str(perm_new) + ghat_str1(p) + ghat_str2(p) + chi_str(p) + ' & ' + str(signs[ind_perm]*weights[ind_perm]) + exp(p)
	print(string_temp)



