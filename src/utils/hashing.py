#I need to combine 3+ techniques to producee a unique number, such as:
#length of the input ^20 minus the length x 2, 
#shift the characters to the left by the amount of vowels, 
#and multiply by the amount of capitals, finally cutting off at 10 digits if longer

#The 4 things a hashing algorithm should do/have:
#Be infeasible to produce a given digest
#Be impossible to revert the digest to the original input
#Slight changes produce drastic differences
#Resulting digest is fixed length

def hash_algorithm(input_string):
    length = len(input_string)
    hash_value = (length ** 20) - (length * 2)
    num_of_capitals = 0
    num_of_vowels = 0
    for i in input_string:
        if i.lower() in 'aeiou':
            num_of_vowels += 1
        if i.isupper():
            num_of_capitals += 1
    if num_of_vowels and num_of_vowels != 0:
        hash_value = hash_value << num_of_vowels
    if num_of_capitals and num_of_capitals != 0:
        hash_value = hash_value * num_of_capitals
    hash_str = str(abs(hash_value))
    if len(hash_str) > 10:
        hash_str = hash_str[:10]
    return hash_str
                 

#ASK SIR IF HASHING ALGORITHM NEEDS IMPROVING
#ADJUST, CURRENTLY NOT COMPLEX ENOUGH