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
    if num_of_capitals != 0:
        hash_value = hash_value * num_of_capitals
    hash_str = str(abs(hash_value))
    if len(hash_str) > 10:
        hash_str = hash_str[:10]
    return hash_str  