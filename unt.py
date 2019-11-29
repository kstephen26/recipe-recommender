f = open("rec1.txt",'r')
lst = []

for line in f:
	if line[0:34] == "https://www.allrecipes.com/recipe/":
		lst.append(line)

print len(lst)