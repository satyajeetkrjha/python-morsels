def interleave(list1,list2):
    for(item1,item2) in zip(list1,list2):
        yield item1
        yield item2