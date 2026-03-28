nums = [1, 2, 3, 4, 5]

# map: square numbers
squared = list(map(lambda x: x**2, nums))
print(squared)

# filter: even numbers
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

from functools import reduce

nums = [1, 2, 3, 4, 5]

sum_all = reduce(lambda a, b: a + b, nums)
print(sum_all)