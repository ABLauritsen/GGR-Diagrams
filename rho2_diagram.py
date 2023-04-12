import numpy as np
import sympy
import itertools
import cmath
from sympy.combinatorics import Permutation


n = 5

k = [sympy.symbols('k%d' % i) for i in range(1,n+1)]
x = [sympy.symbols('x%d' % i) for i in range(1,n+1)]


set_pi_ini = list(itertools.permutations(range(n)))

set_pi_dis = [list(itertools.permutations(range(3))), list(itertools.permutations(range(3,5)))]
# print(set_pi_dis)

disallowed = [ (i + j) for i in set_pi_dis[0] for j in set_pi_dis[1]]

set_pi = []
for pi in set_pi_ini:
	if pi not in disallowed:
		set_pi = set_pi + [pi]


linked = set_pi



no_linked = len(linked)
copies = np.ones(no_linked)




def flip01(perm):
	q = Permutation([1,0],size=n)
	return q*perm*q
	# Permutation([p(perm(p(i))) for i in range(p.size)])

def flip34(perm):
	q = Permutation(n-1,n-2)
	return q*perm*q
	# Permutation([q(perm(q(i))) for i in range(q.size)])

def list_dupliactes(perm):
	out = [perm]
	# for p in out:
	# 	out = out + [flip01(p)]
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




def exp_value(index):
	p = list_reduced[index]
	perm = Permutation(p)
	p = perm.list()
	L = len(p)
	out = (-1)**(int(perm.is_even)+1) * weights[index]
	for j in range(2):
		out = out * sympy.exp(1j * ( k[j] - k[p[j]] + (k[2]-k[p[2]]) / 2 ) * x[j])

	return out



#  Group according to G 
def exp(p, index):
	# out = 'exp(' + str(1j*(k[index] - k[p[index]])*x[index]) + ')'
	out = ' &  ' + sympy.latex(2*(k[index] - k[p[index]]) + k[2]-k[p[2]]) 
	return out

def ghat_str(p):
	return ' &  ' + sympy.latex(k[p[3]] - k[3]) 
	 # + k[4] - k[p[4]]) 

def chi_str(p):
	return ' &  ' + sympy.latex(k[4] - k[p[4]] + k[3] - k[p[3]]) + '=0'

def G_str(p):
	return ' &  ' + sympy.latex(k[2]-k[p[2]]) 


grp_G = [[] for j in range(n)]
# print(grp_G)
for j in range(n):
	for ind_perm in range(no_perm):
		perm = list_reduced[ind_perm]
		p = perm.list()
		p_new = [0] + [a+1 for a in p]
		perm_new = Permutation(p_new)
		if p[2] == j:
			string_temp = '\\\\' + str(perm_new) + G_str(p) + ghat_str(p) + chi_str(p) + '&' + str(signs[ind_perm]*weights[ind_perm]) + exp(p,0) + exp(p,1) 
			grp_G[j] = grp_G[j] + [string_temp]



print('\\hline \\pi &', 
	'\\hat{G}(\\cdots) & \\hat{g}(\\cdots/2) & \\chi(\\cdots) & \\textnormal{weight} &',
	' \\exp\\left(i(\\cdots)\\frac{x_1}{2} \\right) & \\exp\\left(i(\\cdots)\\frac{x_2}{2} \\right)')
for j in range(n):
	print('\\\\ \\hline \\hline')
	for l in grp_G[j]:
		print(l)
print('\\\\ \\hline')
