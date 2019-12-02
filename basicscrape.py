from recipe_scrapers import scrape_me
import ast
import json

# give the url as a string, it can be url from any site listed below

profile_length = 6
recipe_dict = {}
recipe_names = {}
recipe_list = []

def cosine_sim(l1, l2):
	if len(l1) != len(l2):
		return None
	d1 = (sum([x*x for x in l1]))**0.5
	d2 = (sum([x*x for x in l2]))**0.5
	n1 = 0
	for i in range(len(l1)):
		n1 += l1[i]*l2[i]
	return n1/(d1*d2)

def recommend(userprof):
	maxsim = 0
	maxrecipe = "hello"
	for recipe in recipe_dict.keys():
		profile = recipe_dict[recipe]['profile']
		sim = cosine_sim(userprof, profile)
		if sim > maxsim:
			maxsim = sim
			maxrecipe = recipe
	return maxrecipe

recipe_dict = json.load(open("recipe_dict.txt"))
recipe_names = json.load(open("recipe_names.txt"))
recipe_list = list(recipe_dict.keys())
print(recipe_dict)
print(recipe_names)
print(recipe_list)
print("Available Selection:", recipe_names)
print("Select a recipe history using recipe indices above:")
indices = input()
history_lst = [int(x) for x in indices.split(" ")]
print(history_lst)
user_profile = [0]*profile_length
for index in history_lst:
	recipe_profile = recipe_dict[recipe_list[index]]['profile']
	for i in range(profile_length):
		user_profile[i] += recipe_profile[i]

user_profile = [x/profile_length for x in user_profile]

print(recommend(user_profile))



# print(recipe_dict)

