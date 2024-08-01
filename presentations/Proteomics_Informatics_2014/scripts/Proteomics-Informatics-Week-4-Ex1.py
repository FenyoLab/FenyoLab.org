
numlist = [1,2,3,4]

sum = 0
prod = 1

# for num in numlist:
#     sum = sum + num
#     prod = prod * num

for pos in range(len(numlist)):
    sum = sum + numlist[pos]
    prod = prod * numlist[pos]

print "sum: %d\nprod: %d"%(sum, prod)

    
#print sum
#print prod
