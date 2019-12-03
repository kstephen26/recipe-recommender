from recipe_scrapers import scrape_me
import ast
import json
import random
from user import User

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

def userprofile(user):
	recipes = user.favorites
	user_profile = [0]*profile_length
	for recipe in recipes:
		recipe_profile = recipe_dict[recipe]['profile']
		for i in range(profile_length):
			user_profile[i] += recipe_profile[i]
	user_profile = [x/profile_length for x in user_profile]
	user.profile = user_profile
	return user_profile

def contentrecommend(userprof):
	maxsim = 0
	maxrecipe = "hello"
	for recipe in recipe_dict.keys():
		profile = recipe_dict[recipe]['profile']
		sim = cosine_sim(userprof, profile)
		if sim > maxsim:
			maxsim = sim
			maxrecipe = recipe
	return maxrecipe

def useruser(userprof,peer_list):
	similar_peers = []
	k = 5
	for peer in peer_list:
		sim = cosine_sim(userprof, peer.profile)
		similar_peers.append([sim, peer])
	similar_peers = sorted(similar_peers, key=lambda lst: lst[0], reverse = True)
	# print(similar_peers)

	compiled_recipes = {}
	for i in range(k):
		sim, peer = similar_peers[i]
		peer_recipes = peer.favorites
		for recipe in peer_recipes:
			if recipe in compiled_recipes:
				compiled_recipes[recipe] += 1
			else:
				compiled_recipes[recipe] = 1
	# print(compiled_recipes)
	return max(compiled_recipes, key=compiled_recipes.get)
	# print("lcd is: ", lcd)
	# print("occurrence: ", compiled_recipes[lcd])


def create_user():
	user_history = []
	for i in range(100):
		k = random.randint(1,359)
		user_history.append(recipe_names[str(k)])
	new_user = User(user_history)
	return new_user

recipe_dict = json.load(open("recipe_dict.txt"))
recipe_names = json.load(open("recipe_names.txt"))
recipe_list = list(recipe_dict.keys())
# print(recipe_dict)
print(recipe_names)
# print(recipe_list)
print("Available Selection:", recipe_names)
print("Select a recipe history using recipe indices above:")
indices = input()
history_lst = [int(x) for x in indices.split(" ")]
# print(history_lst)


user_list = [create_user() for i in range(20)]
print(user_list)
for user in user_list:
	userprofile(user)

user_profile = [0]*profile_length
for index in history_lst:
	recipe_profile = recipe_dict[recipe_list[index]]['profile']
	for i in range(profile_length):
		user_profile[i] += recipe_profile[i]

user_profile = [x/profile_length for x in user_profile]

print(contentrecommend(user_profile))
print(useruser(user_profile, user_list))
