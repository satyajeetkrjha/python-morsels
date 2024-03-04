def count_words(str):
    res ={}
    splitted_list = str.split()
    splitted_list = [item.lower() for item in splitted_list]
    unique_words = set(splitted_list)
    for word in unique_words:
        res[word] = splitted_list.count(word)
    return res    
        
    
    