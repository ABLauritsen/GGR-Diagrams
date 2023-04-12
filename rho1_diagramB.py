import numpy as np
import sympy
import itertools
import cmath
from sympy.combinatorics import Permutation


n = 4

k = [sympy.symbols('k%d' % i) for i in range(1,n+1)]
x = [sympy.symbols('x%d' % i) for i in range(1,n+1)]


set_pi_ini = list(itertools.permutations(range(4)))

set_pi_dis = [list(itertools.permutations(range(1))), list(itertools.permutations(range(1,4)))]
print(set_pi_dis)

disallowed = [ (i + j) for i in set_pi_dis[0] for j in set_pi_dis[1]]

set_pi = []
for pi in set_pi_ini:
	if pi not in disallowed:
		set_pi = set_pi + [pi]


linked = set_pi
print(len(set_pi))
for p in set_pi:
	perm = Permutation([0] + [a+1 for a in p])
	print(perm)


no_linked = len(linked)
copies = np.ones(no_linked)

def flip23(perm):
	q = Permutation([0,2,1],size=n)
	return q*perm*q

def flip24(perm):
	q = Permutation(1,3)
	return q*perm*q

def flip34(perm):
	q = Permutation(2,3)
	return q*perm*q

# for p in set_pi:
# 	perm = Permutation(p)
# 	print(perm, flip24(perm))

def list_dupliactes(perm):
	out = [perm]
	for p in out:
		out = out + [flip24(p)]
	for p in out:
		out = out + [flip23(p)]
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

print(no_perm)

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

def Ghat_str1(p):
	return ' & ' + sympy.latex(k[1] - k[p[1]])

def Ghat_str2(p):
	return ' & ' + sympy.latex(k[1] - k[p[1]] + k[3] - k[p[3]])

def chi_str(p):
	return ' &  ' + sympy.latex(k[1] - k[p[1]] + k[2] - k[p[2]] + k[3] - k[p[3]]) + '=0'





print('\\hline \\pi & \\hat{G}(\\cdots, & \\cdots) & \\chi(\\cdots) & \\textnormal{weight} & \\exp(i(\\cdots)x_1)')

for ind_perm in range(no_perm):
	perm = list_reduced[ind_perm]
	p = perm.list()
	p_new = [0] + [a+1 for a in p]
	perm_new = Permutation(p_new)

	string_temp = '\\\\' + str(perm_new) + Ghat_str1(p) + Ghat_str2(p) + chi_str(p) + ' & ' + str(signs[ind_perm]*weights[ind_perm]) + exp(p)
	print(string_temp)



