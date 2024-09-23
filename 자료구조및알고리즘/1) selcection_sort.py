def selection_sort(array):
    for i in range(0,len(array)):
        for j in range(i,len(array)):
            min_num = array[i]
            if min_num > array[j]:
                min_index = j
        array[i], array[min_index] = array[min_index], array[i]

#input array
array = [3,5,6,7,88,5,2]

selection_sort(array)
print(array)
