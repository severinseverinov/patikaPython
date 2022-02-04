def flatten (a,b):

    for i in a:
        if type(i) != type([]):
            b.append(i)
        elif type(i) == type([]):
            flatten(i, b)
    return b


arr = [[1,'a',['cat'],2],[[[3]],'dog'],4,5]
f_list = []
 
print(flatten(arr, f_list))