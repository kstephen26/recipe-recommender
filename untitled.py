f = open("rec1.txt",'r')

i = 0
lst = []

for line in f:
	if line[0:34] == "https://www.allrecipes.com/recipe/":
		i += 1
		lst.append(line)

f.close()

print i
print len(lst)