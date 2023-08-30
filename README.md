Python-script for computing the values of small diagrams in the Gaudin-Gilespie-Ripka (GGR) expansion.

The GGR expansion is explained in the papers:  
 - *Almost optimal upper bound for the ground state energy of a dilute Fermi gas via cluster expansion*    
A. B. Lauritsen, [arXiv:2301.08005](https://doi.org/10.48550/arXiv.2301.08005)

 - *Ground state energy of the dilute spin-polarized Fermi gas: Upper bound via cluster expansion*    
A. B. Lauritsen and R. Seiringer, [arXiv:2301.04894](https://doi.org/10.48550/arXiv.2301.04894)

The script takes as input a graph and outputs all equivalence classes of quasi-linked permutations, meaning permutations with each linked component having at least one external vertex.   

Two permutations/diagrams are equivalent if they have the same value. 
This happens if the permutations are related by a symmetry of the graph. For each equivalence class is computed the *weight* being the sign times the number of equivalent permutations in the equivalence class.
