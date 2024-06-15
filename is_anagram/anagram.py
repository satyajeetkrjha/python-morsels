
# def is_anagram(word1,word2):
#     return sorted(word1) == sorted(word2)


#Bonus 2 

#removes spaces and all in word and makes a sorted string
def letters_in(string):
    return sorted(char for char in string.lower() if char.isalpha())


def is_anagram(word1,word2):
    return letters_in(word1) == letters_in(word2)
