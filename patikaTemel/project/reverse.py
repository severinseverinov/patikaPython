def reversed_list (arr):
    
    for i in range(len(arr)):
        if type(arr[i]) == type([]):
            arr[i] = arr[i][::-1]
            reversed_list(arr[i])
    
    return (arr[::-1])


arr = [[1, 2], [3, 4], [5, 6, 7]]
print(reversed_list(arr))