# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #number of <pos> tags possible by number of <pos> tags possible

    unique_tags = dict()
    inverse_unique_tags = []
    tag_index = 0
    word_emissions = dict()
    word_em_index = 0
    #loop over training set to get all words, pos's that appear
    for file in training_list:
        with open("../training-test/"+file, "r") as a_file:
            for line in a_file:
                x = line.split(":")

                #special case of emission being a colon
                
                if len(x) == 3:
                    colon = ": "
                    if not (colon in word_emissions):
                        word_emissions[colon] = word_em_index
                        word_em_index += 1
                    if not (x[-1] in unique_tags):
                        unique_tags[x[-1]] = tag_index
                        inverse_unique_tags.append(x[-1])
                        tag_index += 1

                #emission is not a colon
                else:
                    if not (x[0] in word_emissions):
                        word_emissions[x[0]] = word_em_index
                        word_em_index += 1
                    
                    if not (x[1] in unique_tags):
                        unique_tags[x[1]] = tag_index
                        inverse_unique_tags.append(x[1])
                        tag_index += 1

    #define sizes of matrix
    K = len(unique_tags)
    N = len(word_emissions)
    matrix_trans_bt_hidden = np.zeros((K,K))

    #observe oj 
    matrix_em_given_state = np.zeros((K,N))
    #that state x1 is this part of speech
    initial_probabilities = np.zeros(K)
    #come up with the probability tables
    counter = 0
    for file in training_list:
        with open("../training-test/"+file, "r") as a_file:
            last_pos = None
            for line in a_file:
                #deal with posibility of a colon
                if line[0] == ":":
                    x = line.split(":")
                    #part of speech
                    pos = x[-1]
                    #word, observed
                    emission = ": "
                else:
                    x = line.split(":")
                    #part of speech
                    pos = x[1]
                    #word, observed
                    emission = x[0]

                #set initial probabilities
                if (not last_pos) or last_pos == " PUN\n":
                    initial_probabilities[unique_tags[pos]] += 1 
                #increment entry in matrix
                matrix_em_given_state[unique_tags[pos]][word_emissions[emission]] += 1
                #if last word exists
                if last_pos:
                    matrix_trans_bt_hidden[unique_tags[last_pos]][unique_tags[pos]] += 1
                #update last word
                last_pos = pos

    #sanity check for probabilities-------------------------------------------------
    # print(inverse_unique_tags)
    # print()
    # print(f"Unique: tags: {unique_tags}")
    # print()
    # print(word_emissions)
    # print()
    # print(f"Initial: {initial_probabilities}")
    # print()
    # print(f"Counts between states: {matrix_trans_bt_hidden}")
    # print()
    # print(f"Counts state to emission: {matrix_em_given_state}")
    #--------------------------------------------------------------------------------

    

    #normalize our cpts
    for i in range(K):
        total = sum(matrix_trans_bt_hidden[i])
        for j in range(K):
            matrix_trans_bt_hidden[i][j] = matrix_trans_bt_hidden[i][j]/total
    for i in range(K):
        total = sum(matrix_em_given_state[i])
        for j in range(N):
            matrix_em_given_state[i][j] = matrix_em_given_state[i][j]/total
    total = sum(initial_probabilities)
    for i in range(K):
        initial_probabilities[i] = initial_probabilities[i]/total
    #check proper normalization----------------------------------------
    # print(initial_probabilities)  
    # print(matrix_trans_bt_hidden)
    # print(matrix_em_given_state)
    #------------------------------------------------------------------

    #THE CODE FROM HELL
    #----------------------------------------------------------------------------------------------------------------------
    test_emissions = list()
    #TODO: Will eventually have to deal with possibility of never before seen emission
    with open("../training-test/"+test_file, "r") as a_file:
        for line in a_file:
            x = line.split("\n")
            test_emissions.append((x[0]+ " "))

    print(f"Len test sequence: {len(test_emissions)}")

    #viterbi finally executes, does it work,idk but at least it runs
    prob_treb, path_treb = viterbi(test_emissions, unique_tags, initial_probabilities, matrix_trans_bt_hidden, matrix_em_given_state, word_emissions)
    # print(len(prob_treb))
    # print(prob_treb)

    max_probs_indices = np.argmax(prob_treb, axis=0)
    print(max_probs_indices)

    test_tags = []
    #loop over all test emission, and pick the most probable one
    for i in range(len(test_emissions)):
        tag = inverse_unique_tags[max_probs_indices[i]]
        test_tags.append(tag)
    # print(f"Test tags: {test_tags}")
    
    #now we loop over our test_tags, and test_emission simultanously and concat them with a test_emssions[i]:test_tags[i]
    with open("../autograder/"+output_file, "w") as a_file:
        for i in range(len(test_emissions)):
            a_file.write(test_emissions[i]+":"+test_tags[i])
    print("Done")
    return


def viterbi(O,S,pi, A, B, dict_emission):
    #initialize appropriate matrices
    prob_treb = np.zeros((len(S),len(O)))
    path_treb = np.empty((len(S),len(O)), dtype=object)

    for s in range(len(S)):
        prob_treb[s][0] = pi[s] * B[s][dict_emission[O[0]]]
        path_treb[s][0] = [s]
    
    #normalize first filled column
    normalize(prob_treb, col=0)
    #loop over test sequence
    for o in range(1, len(O)):

        for s in range(len(S)):
            #TODO: add a try catch to handle unseen words
                x = get_max_arg(len(S), prob_treb, A, B,o,s, dict_emission,O) 
                prob_treb[s][o] = prob_treb[x][o-1]*A[x][s]*B[s][dict_emission[O[o]]]
                path_treb[s][o] = path_treb[x][o-1]
                path_treb[s][o].append(s)
        
        #normalize the col just filled in
        normalize(prob_treb, col=o)
    
    return prob_treb, path_treb

def get_max_arg(K, prob_treb, A,B,o,s, dict_emission,O):
    max_index = -1
    max_prob = -1
    for x in range(0, K):
        pot_max = prob_treb[x][o-1]*A[x][s]*B[s][dict_emission[O[o]]]
        if pot_max > max_prob:
            max_prob = pot_max
            max_index = x
    return max_index

#normalize column
def normalize(prob_treb, col=0):
    values = prob_treb.sum(axis=0)
    amount = values[col]
    prob_treb[:,col] = prob_treb[:,col]/amount
    return


if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)