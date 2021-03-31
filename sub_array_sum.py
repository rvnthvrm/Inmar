'''
Given an array of positive numbers 
and a positive number ‘k’, 
find the maximum sum of any contiguous subarray of size ‘k’.
'''
lst = [30, 4, 2, 10, 2, 3, 1, 1, 20, 40]
key = 3
f = []

def sum_subarray(key):
	if (len(lst) < key):
		return 0

	res = 0
	for i in range(key):
		res += lst[i]

	return res

for i in range(len(lst)):
	f.append(sum_subarray(key))
	del lst[0]

print(max(f))
