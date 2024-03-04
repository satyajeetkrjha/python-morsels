
def parse_ranges(str_range):
    res =[]
    for item in str_range.split(','):
        start,end =item.split('-')
        for num in range(int(start),int(end)+1):
            yield num  
    return res        


def parse_ranges(str_range):
    pairs =[group.split('-') for group in str_range.split(',')]
    for start,stop in pairs:
        yield from range(int(start),int(stop))
    
