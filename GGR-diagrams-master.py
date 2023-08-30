import numpy as np
import sympy
import itertools
import cmath
from sympy.combinatorics import Permutation
import igraph as ig 
# -------------------------------------------------
# -------------------------------------------------
# -------------------------------------------------
# -------------------------------------------------

# Number of external vertices 
n_ext = 1

# List all edges [i, j] of the graph.
# Vertices are labelled 1, 2, ..., n
list_g_edges = [ [2,3], [3,4], [2,4] ]



# What to print in the table
# Fill out as needed
# -------------------------------------------------
N = max(max(list_g_edges)) + 1
k = [sympy.symbols('k%d' % i) for i in range(1,N)]
# x = [sympy.symbols('x%d' % i) for i in range(1,N)]
# -------------------------------------------------

# Define string to fill table header
string_table = str()

# Define string to print for each permutation
def string_print(perm):
	return str()




# -------------------------------------------------
# -------------------------------------------------
# -------------------------------------------------
# -------------------------------------------------
# Start counting at 0 and define graph
edges = sorted([ sorted([i[0]-1,i[1]-1]) for i in list_g_edges ])
graph = ig.Graph(edges = edges)
n = max(max(edges)) + 1
# print(graph)
print('Number of vertices:', n)
print('Edges:', sorted([sorted(j) for j in list_g_edges]))



# ---------------------------------
# Generate permutation from partial list (i.e. from list-form of permutation of subset)
def generate_perm(list_, n):
	list_replace = list(range(n))
	list_sorted = sorted(list_)

	out_list = list_replace
	ind = 0

	for i in range(n):
		if i in list_:
			out_list[i] = list_[ind]
			ind += 1

	# print(list_, 'turned to: ', out_list, 'cycle form:', str(Permutation(out_list)))

	return Permutation(out_list)
# ---------------------------------



# Find all symmetries
# ----------------------------------
set_p_graph = [ generate_perm(list(j), n).array_form for j in list(itertools.permutations(range(n_ext, n)))]
# print(set_p_graph)


list_sym_p_graph = []

def new_edge(edge, p):
	return [ p[edge[0]], p[edge[1]] ]


for p in set_p_graph:
	new_edges = sorted([sorted(new_edge(edge, p)) for edge in edges])
	new_graph = ig.Graph(new_edges)
	# print('compare:', graph, new_graph)
	if new_graph.get_edgelist() == graph.get_edgelist():
		list_sym_p_graph = list_sym_p_graph + [p]

# print(list_sym_p_graph)
# print('perms:', [str(Permutation(p)) for p in list_sym_p_graph])
# ----------------------------------



# Find connected components
# -----------------------------------
con_cmp = graph.connected_components()
# print(con_cmp)
# print(list(con_cmp))

print('Connected components:', [ list(np.array(i) + (np.ones(len(i), dtype=int))) for i in list(con_cmp)])


# Remove singleton external vertices
to_be_removed = []

for j in range(len(con_cmp)):
	if len(con_cmp[j]) == 1:
		to_be_removed = to_be_removed + [con_cmp[j]]
		if con_cmp[j][0] >= n_ext:
			print('Error. Internal vertices must have degree >= 2')

con_cmp = [j for j in con_cmp if j not in to_be_removed]



# Check if all external vertices removed. If so, add them as the first cluster. Else, add the removed to the first cluster.
if all(j not in con_cmp[0] for j in list(range(n_ext)) ):
	con_cmp = [list(range(n_ext))] + con_cmp
else:
	con_cmp[0] = sorted(np.unique(con_cmp[0] + list(range(n_ext))))

print('"Connected" components after grouping external vertices:', [ list(np.array(i) + (np.ones(len(i), dtype=int))) for i in list(con_cmp)])
list_n_clusters = [len(j) for j in con_cmp]
n_clusters = len(con_cmp)
# -----------------------------------









# Find all non-linked permutations.
# ---------------------------------
set_pi_dis = []

for cluster in range(n_clusters):
	low_lim = sum([list_n_clusters[j] for j in range(cluster)])
	up_lim = low_lim + list_n_clusters[cluster] - 1

	other_vertices = list(range(low_lim)) + list(range(up_lim+1,n))

	# print([low_lim, up_lim], other_vertices)
	set_pi_dis = set_pi_dis + [ [list(itertools.permutations(range(low_lim,up_lim+1))), list(itertools.permutations(other_vertices))] ]
		


disallowed = []
for ind in range(n_clusters):
	in_cluster_perms = [ generate_perm(list(j), n) for j in set_pi_dis[ind][0] ]
	outside_cluster_perms = [ generate_perm(list(j), n) for j in set_pi_dis[ind][1] ]
	disallowed = disallowed + [ (i * j) for i in in_cluster_perms for j in outside_cluster_perms ]


# Clear disallowed permutations if graph is connected
if n_clusters == 1:
	disallowed = []


# Change to array-form
disallowed = [j.array_form for j in disallowed]
# ---------------------------------



# Generate list of linked permutations. (In list form.)
# ---------------------------------
set_pi_ini = [ list(j) for j in list(itertools.permutations(range(n)))]
set_pi = []
for pi in set_pi_ini:
	if pi not in disallowed:
		set_pi = set_pi + [pi]

linked = set_pi

no_linked = len(linked)
copies = np.ones(no_linked)


# print(disallowed)
print('Number of initial permutations = n! =', len(set_pi_ini))
# print(len(disallowed))
print('Number of quasi-linked permutations =', no_linked)
# print([str(Permutation(Permutation(j).list(size=-1))) for j in linked])
# ---------------------------------



# Find all equivalent permutations
def list_duplicates(perm):
	out = [perm]

	# Duplicates from graph symmetries
	for p in out:
		for q in list_sym_p_graph:
			out = out + [ Permutation(q) * p * (~Permutation(q)) ]

	# Duplicate due to p and p inverse giving same value:
	for p in out:
		out = out + [~p]

	return out


# Find all non-equivalent diagrams
# ---------------------------------
list_reduced = []
weights = []

for i in range(no_linked):
	perm = Permutation(linked[i])

	list_copies = [perm]
	for p in list_duplicates(perm):
		if p not in list_copies:
			list_copies = list_copies + [p]

	if all(item not in list_reduced for item in list_copies):
		list_reduced = list_reduced + [perm]
		weights = weights + [len(list_copies)]


no_perm = len(list_reduced)
print('Number of non-equivalent quasi-linked permutations =', no_perm)

signs = np.zeros(no_perm,dtype=int)


for i in range(no_perm):
	perm = list_reduced[i]
	# print(perm)
	p = Permutation(perm)
	sigma = (-1)**(int(p.is_even)+1)
	# print(sigma)
	signs[i] = sigma
# ---------------------------------






# # Printing the table
# -----------------------------



# Simplify cycle form of permutation.
def print_form(p):
	# p of list form
	return str(Permutation(Permutation(p).list(size=-1)))


# Print the table 
# ---------------------------------
print()
print('Table:')
print()
print('\\newcolumntype{L}{>{$\\displaystyle}Sl<{$}}')
print('\\begin{tabular}{|L|L|L|}')
print('\\hline \\pi & \\textnormal{weight} &', string_table)

print('\\\\ \\hline \\hline')

for ind_perm in range(no_perm):
	perm = list_reduced[ind_perm]
	p = perm.list()
	p_new = [0] + [a+1 for a in p]
	perm_new = Permutation(p_new)
	string_temp = print_form(p_new) + ' & ' + str(signs[ind_perm]*weights[ind_perm]) + ' & ' + string_print(perm)
	print(string_temp)
	print('\\\\ \\hline')

print('\\end{tabular}')

print()






# #   Make diagram pictures
# -----------------------------------



# Vertices:
# ---------------------------------
scale = 1
scalebox_factor = 1
# scale = (n/2)**(1/2)
# scalebox_factor = (n/2)**(-1/2) 

zeta = cmath.exp(1j * 2 * cmath.pi / n)

vertices = [ [scale * (zeta**l).real, scale * (zeta**l).imag] for l in range(n) ]

angle_shift = 180 / cmath.pi * cmath.phase(zeta)
# ---------------------------------


# Initial and ending part of diagram drawings
ini_dia = '\\vcenter{\\hbox{\\begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=1.0cm,y=1.0cm] '
end_dia = '\\end{tikzpicture} }} \\qquad'


# Draw the graph of g-edges
def base_graph():
	for l in range(n):
		print('\\node (' + str(l+1) + ') at ' + str(tuple(vertices[l])) + ' {$' + str(l+1) + '$}; ')
	for l in range(n_ext):
		print('\\node [anchor = ' + str(180 + angle_shift * l) + '] at (' + str(l+1) + ') {$*$};')
	for edge in edges:
		i = edge[0] + 1
		j = edge[1] + 1
		print('\\draw[dashed] (' + str(i) + ') to (' + str(j) + ');')


# Drawing the permutation
def pic(p_new):
	for j in range(1,n+1):
		if p_new[j] != j:
			edge_temp = tuple(sorted([j-1, p_new[j]-1]))
			# print(edge_temp)
			if edge_temp in graph.get_edgelist() or p_new[p_new[j]] == j:
				print(' \\draw[->] (' + str(j) + ') to[bend right] (' + str(p_new[j]) + ');')
			else:
				print(' \\draw[->] (' + str(j) + ') to (' + str(p_new[j]) + ');')
			# print(' \\draw[->] (' + str(j) + ') to[bend right] (' + str(p_new[j]) + ');')


# Drawing the diagrams
print('Diagrams:')
print()
print('\\[')

temp = 0
for ind_perm in range(no_perm):
	perm = list_reduced[ind_perm]
	p = perm.list()
	p_new = [0] + [a+1 for a in p]
	perm_new = Permutation(p_new)

	print( print_form(p_new), ' : \\quad')
	print('\\scalebox{' + str(scalebox_factor) + '}{$')
	print(ini_dia)
	base_graph()
	pic(p_new)
	print(end_dia)
	print('$}')

	temp += 1

	if temp % 3 == 0:
		print('\\]')
		print('\\[')

print('\\]')
print()


