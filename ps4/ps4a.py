# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def conc_string(a, b, pos):
    '''
    b is single char, pos is b position in the new string
    '''
    if pos == len(a):
        return a + b
    else:
        res = []
        for i, c in enumerate(a):
            if i == pos:
                res.append(b)
            res.append(c)
            
        return "".join(res)
            

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]
    else:
        # Recursion
        res = []
        for s in get_permutations(sequence[1:]):
            for k in range(len(s)+1):
                res.append(conc_string(s, sequence[0], k))
            #res.append(sequence[0] + s)
            #res.append(s + sequence[0])
        return res
    

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
   # print(conc_string("caca", "o", 0))
    res = get_permutations('abcd')
    print(res)
    pass #delete this line and replace with your code here

