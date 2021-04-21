#!/usr/bin/env python

'''
Python script to read 1-factorizations of K_{12} from Kaski and Ostergard.
The script then checks the C_4 condition.
Written by Philip DeOrsey, Stephen Hartke and Jason Williford, 2021.

The file of 1-factorizations of K_{12} from Kaski and Ostergard has the following format.
Each 1-factorization is 13 lines: 12 lines of data and 1 blank line.
The 12 lines of data give a 12 rows x 11 columns matrix with entries from 0..5.
Each column corresponds to one of the 11 1-factors in the 1-factorization.
The rows represent the vertices.  Entry i,j has value c if in 1-factor j,
vertex i is an endpoint of edge c.

The first incidence matrix in the file is:
00000000000
01111111111
10122222222
11033333333
22201234444
23310325555
32344440123
33255551032
44423454501
45532545410
54545012345
55454103254

'''


import sys
import numpy as np
import itertools


class C4Violation(Exception):
    '''Exception raised when a C_4 violation is detected.  This allows to break out of several layers of loops.'''
    pass

class EndOfFile(Exception):
    '''Exception raised when no more lines can be read from the input file.'''
    pass



if __name__=="__main__":
    
    if len(sys.argv)<3:
        print("USAGE: read_1factorizations.py data_file.txt output.txt; use - for stdin for input")
        exit(99)
    
    file_input =sys.argv[1]
    file_output=sys.argv[2]
    
    # encoding for outputted 1-factorizations
    output_char=([str(i) for i in range(10)]+
                 [chr(i+ord('A')) for i in range(26)])
    
    
    n=12  # number of vertices, we are looking at 1-factorizations of K_n
    num_edges_in_1_factor=n//2  # number of edges in a 1-factor of K_n
    num_1_factors=n-1  # number of 1-factors in a 1-factorization of K_n
    
    incidence_matrix=np.zeros((n,num_1_factors),dtype=np.int64)  # matrix read straight from the file
    adjacency_matrix=np.zeros((n,n),dtype=np.int64)
        # adjacency_matrix, where entry i,j is the color of the edge between vertex i and vertex j.
    edge_matrix=np.zeros((num_1_factors,num_edges_in_1_factor,2),dtype=np.int64)
        # edge matrix, where entry i,j,k is 1-factor i, edge j, endpoint k.  Note that k=0,1.
    
    
    if file_input=='-':
        file_in=sys.stdin
    else:
        file_in=open(file_input,'rt')
        
    with open(file_output,'wt') as file_out:
        
        num_tested=0  # number of 1-factorizations tested
        num_good=0    # number of 1-factorizations that pass the C_4 test
        
        try:
            while True:
                
                # read in a 1-factorization
                for i in range(n):
                    line=file_in.readline()
                    if not line:  # we have reached the end of the file
                        raise EndOfFile
                    for j in range(num_1_factors):
                        incidence_matrix[i,j]=np.int64(line[j])
                _=file_in.readline()  # should be a blank line
                
                num_tested+=1
                if (num_tested % 100000)==0:
                    print(f"num_tested={num_tested:11,}  num_good={num_good:3}")
                
                
                # update the adjacency and edge matrices
                for f in range(num_1_factors):
                    for e in range(num_edges_in_1_factor):
                        # in column f, find the first entry (will be set to i) equal to e; is in row at least e
                        i=e
                        while incidence_matrix[i,f]!=e:
                            i+=1
                        # in column f, find the first entry (will be set to j) equal to e that is beyond row i
                        j=i+1
                        while incidence_matrix[j,f]!=e:
                            j+=1
                        # in 1-factor f, the e-th edge has endpoints i and j
                        edge_matrix[f,e,0]=i
                        edge_matrix[f,e,1]=j
                        
                        adjacency_matrix[i,j]=adjacency_matrix[j,i]=f  # edge i,j is in 1-factor f
                
                
                # test the C_4 condition
                try:
                    for f in range(num_1_factors-1):  # choose a 1-factor f
                        # Note that we don't need to test the last 1-factor.
                        
                        # choose a pair e1,e2 of edges from f
                        for e1 in range(num_edges_in_1_factor):  # choose the first edge
                            # a,b are the endpoints of e1
                            a=edge_matrix[f,e1,0]
                            b=edge_matrix[f,e1,1]
                            
                            for e2 in range(num_edges_in_1_factor):  # choose the second edge
                                # c,d are the endpoints of e2
                                c=edge_matrix[f,e2,0]
                                d=edge_matrix[f,e2,1]
                                
                                # if exactly one of the other pairs of independent edges is monochromatic,
                                # then we have a violation of the C_4 condition
                                if ( (adjacency_matrix[a,c]==adjacency_matrix[b,d]) !=
                                     (adjacency_matrix[a,d]==adjacency_matrix[b,c])    ):
                                    raise C4Violation
                    
                    # this 1-factorization passed the C_4 test, and hence is good
                    num_good+=1
                    print(f"num_tested={num_tested:11,}  num_good={num_good:3}  We have found a new good 1-factorization!")
                    
                    # save a string of the upper-right triangular part of the adjacency matrix, read off by columns (colex order).
                    s=''
                    for j in range(n):
                        for i in range(j):
                            s+=output_char[adjacency_matrix[i,j]]
                    file_out.write(s+"\n")
                    
                    
                except C4Violation:  # this is a convenient way to break out of the nested for loops
                    pass
        
        except EndOfFile:
            pass
    
    file_in.close()
    print(f"num_tested={num_tested:11,}  num_good={num_good:3}  Done, these are the total tested and good.")
