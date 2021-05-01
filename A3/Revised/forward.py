import pandas as pd
import numpy as np

V = np.array([0, 1, 2, 3]) 

# Transition Probabilities
a = np.array(((0.1, 0.4, 0.5), (0.3,0.3,0.4),(0.3,0.5,0.2)))

# Emission Probabilities
b = np.array(((0.7, 0.2, 0.05,0.05), (0.3, 0.3, 0.2,0.2),(0.1, 0.3, 0.4,0.2)))

# # Equal Probabilities for the initial distribution

#gym, library, pub
pi = np.array((0.3, 0.5, 0.2))

def viterbi(O,S,pi, A, B):
    print(f"V: {O}")
    print(len(S))
    #initialize appropriate matrices
    prob_treb = np.zeros((len(S),len(O)))
    path_treb = np.empty((len(S),len(O)), dtype=object)
    # print("Before: ")
    for s in range(len(S)):
        # print(s)
        # print(B[s,O[0]])
        prob_treb[s,0] = pi[s] * B[s,O[0]]
        path_treb[s,0] = [s]
    # print("After: ")
    #normalize first filled column
    normalizer(prob_treb, col=0)
    #loop over test sequence
    for o in range(1, len(O)):
        # print(f"o:{o}")
        for s in range(len(S)):
            #TODO: add a try catch to handle unseen words
                x = get_max_arg(len(S), prob_treb, A, B,o,s,O) 
                prob_treb[s,o] = prob_treb[x,o-1]*A[x,s]*B[s,O[o]]
                path_treb[s,o] = path_treb[x,o-1].copy()
                path_treb[s,o].append(s)
        
        #normalize the col just filled in
        normalizer(prob_treb, col=o)
    
    return prob_treb, path_treb

def get_max_arg(K, prob_treb, A,B,o,s,O):
    max_index = -1
    max_prob = -1
    for x in range(0, K):
        pot_max = prob_treb[x][o-1]*A[x][s]*B[s][O[o]]
        if pot_max > max_prob:
            max_prob = pot_max
            max_index = x
    return max_index
def normalizer(prob_treb, col=0):
    values = prob_treb.sum(axis=0)
    amount = values[col]
    if amount == 0:
        print(col)
        print(prob_treb[:,204])
        print(values)
        print(values[203])
    prob_treb[:,col] = prob_treb[:,col]/amount
    return
def normalize(alpha, row=0):
    norm = np.sum(alpha[row])
    alpha[row] = alpha[row]/norm

def forward(V, a, b, pi):
    alpha = np.zeros((V.shape[0], a.shape[0]))
    alpha[0, :] = pi * b[:, V[0]]
    # normalize(alpha, row=0)
    for t in range(1, V.shape[0]):
        for j in range(a.shape[0]):
            alpha[t, j] = alpha[t - 1].dot(a[:, j]) * b[j, V[t]]
        # normalize(alpha, row=t)

    return alpha

alpha = forward(V, a, b, pi)

print(alpha)
for i  in range(len(alpha)):
	norm = np.sum(alpha[i])
	alpha[i] = alpha[i]/norm
print()
print(alpha)
print(alpha.argmax(axis=1))

print("-----------------------------------------")

S = [0]*a.shape[0]
alpha, paths = viterbi(V,S,pi, a, b)
print(alpha)
print(paths.transpose())
