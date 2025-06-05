def common_elements(list1, list2):
    return [item for item in list1 if item in list2]

print(common_elements([4, 'apple', 10, 'hi', 3], [23, 'apple', 5, 9, 3]))
