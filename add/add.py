def add(matrix1,matrix2):
    res=[]
    for row1,row2 in zip(matrix1,matrix2):
        print(f"row1 is {row1} and row2 is {row2}")
        row =[]
        for item1 ,item2 in zip(row1,row2):
            print(f"item1 ={item1} and item2 ={item2}")
            row.append(item1+item2)
        res.append(row)
    return row        
           