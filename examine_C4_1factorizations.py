#!/usr/bin/env python

'''
Python script to examine 1-factorizations of K_{12} that pass the C_4 test.
This script applies the two K_4-e test.
The script reads in the output of read_1factorizations.py.
Written by Philip DeOrsey, Stephen Hartke, and Jason Williford, 2021.
'''


import sys
import numpy as np
import itertools


class K4meViolation(Exception):
    '''Exception raised when a 2 K_4-e violation is detected.  This allows to break out of several layers of loops.'''
    pass


if __name__=="__main__":
    
    if len(sys.argv)<3:
        print("USAGE: examine_C4_1factorizations.py output.txt final.txt")
        exit(99)
    
    file_input =sys.argv[1]
    file_output=sys.argv[2]
    
    # encoding for outputted 1-factorizations
    output_char=([str(i) for i in range(10)]+
                 [chr(i+ord('A')) for i in range(26)])
    
    with open(file_input,'rt') as file_in:
        with open(file_output,'wt') as file_out:
            
            num_tested=0  # number of 1-factorizations tested that have already passed the C_4 test
            num_good=0    # number of 1-factorizations that pass the 2 K_4-e test
            while True:
                line=file_in.readline().strip()
                if not line:  # we have reached the end of the file
                    break
                
                if len(line)==12*(12-1)//2:
                    n=12  # number of vertices, we are looking at 1-factorizations of K_n
                else:
                    print(f"Can't determine n from the input file; len={len(line)}")
                    exit(5)
                
                num_edges_in_1_factor=n//2  # number of edges in a 1-factor of K_n
                num_1_factors=n-1  # number of 1-factors in a 1-factorization of K_n
                
                adjacency_matrix=np.zeros((n,n),dtype=np.int64)
                    # adjacency_matrix, where entry i,j is the color of the edge between vertex i and vertex j.
                
                # re-create the upper-right triangular part of the adjacency matrix, read off by columns (colex order).
                pos=0
                for j in range(n):
                    for i in range(j):
                        f=output_char.index(line[pos])  # which 1-factor the edge i,j is in
                        adjacency_matrix[i,j]=adjacency_matrix[j,i]=f
                        pos+=1
                
                num_tested+=1
                print(f"num_tested={num_tested:3}  num_good={num_good:1}")
                
                
                # test the 2 K_4-e condition
                V=set(range(n))  # the vertex set
                
                try:
                    for c,C in enumerate(itertools.combinations(V,4)):
                        # choose 4 unordered vertices
                        
                        if c%100==0:
                            print("   testing ",c,C)
                        
                        for P in itertools.permutations(V-set(C),4):
                            # choose 4 ordered vertices in the remaining vertices V-C
                            
                            # count the number of corresponding edges that have the same color
                            count=0
                            for e in itertools.combinations(range(4),2):  # edges from a K_4
                                if (adjacency_matrix[C[e[0]],C[e[1]]]==
                                    adjacency_matrix[P[e[0]],P[e[1]]]  ):
                                    count+=1
                            if count==5:
                                # This 1-factorization fails the 2 K_4-e test.
                                raise K4meViolation
                    
                    # this 1-factorization passed the 2 K_4-e test, and hence is good
                    num_good+=1
                    print(f"num_tested={num_tested:3}  num_good={num_good:1}  We have found a new good 1-factorization!")
                    
                    # print out the lists of edges in each 1-factor of the 1-factorization
                    for f in range(num_1_factors):
                        s=chr(ord('A')+f)+': ['
                        for i in range(n):
                            for j in range(i+1,n):
                                if adjacency_matrix[i,j]==f:
                                    s+=f"({i},{j})"
                                    s+=(',' if j<n-1 else '')
                        s+=']'
                        file_out.write(s+"\n")
                    file_out.write("\n")
                
                except K4meViolation:
                    # this 1-factorization did not pass the test
                    pass
    
    print(f"num_tested={num_tested:3}  num_good={num_good:1}  Done, these are the total tested and good.")
