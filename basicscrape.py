from recipe_scrapers import scrape_me
import ast
import json
import random
from user import User

# give the url as a string, it can be url from any site listed below

profile_length = 8
recipe_dict = {}
recipe_names = {}
recipe_list = []
recipe_dict = json.load(open("recipe_dict.txt"))
recipe_names = json.load(open("recipe_names.txt"))
recipe_namesrev = {}
for number in recipe_names:
	recipe_namesrev[recipe_names[number]] = number
# print(recipe_namesrev)

recipe_list = list(recipe_dict.keys())

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
	reclist = []
	for recipe in recipe_dict.keys():
		profile = recipe_dict[recipe]['profile']
		sim = cosine_sim(userprof, profile)
		reclist.append([recipe,sim])
		# if sim > maxsim:
		# 	maxsim = sim
		# 	maxrecipe = recipe
	reclist = sorted(reclist, key=lambda lst: lst[1], reverse = True)
	reclist = [x[0] for x in reclist]
	return reclist[:5]

def itemitemcollab(idea, history, k):
	# idea is the index of a recipe idea, history is the list of index and rating tuples of recipes cooked in the past. k is neighborhood size.
	reclist = []
	userprof = recipe_dict[recipe_names[idea]]['profile']
	history_length = len(history)
	for recipe, rating in history:
		profile = recipe_dict[recipe_names[str(recipe)]]['profile']
		sim = cosine_sim(userprof,profile)
		reclist.append([recipe,sim,rating])
	reclist = sorted(reclist, key=lambda lst: lst[1], reverse = True)
	# reclist = [x[0] for x in reclist]
	num = 0
	denom = 0
	for i in range(k):
		num += reclist[i][1]*reclist[i][2]
		denom += abs(reclist[i][1])
	rating = num/denom
	return rating
	

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
# print(recipe_dict)
# print(recipe_names)
# print(recipe_list)
# print("Available Selection:", recipe_names)
# print("Select a recipe history using recipe indices above:")
# indices = input()

system_type = 'Item-Item'

if system_type == 'Item-Item':
	print("How many recipes would you like to add to your recipe history (at least 5)?")
	history_length = int(input())
	print("Selection: ", recipe_names)
	history_lst = [[0,0]]*history_length
	for i in range(history_length):
		print("Enter a recipe number and rating from the above selection separated by a space.")
		history_lst[i] = [int(x) for x in input().split(" ")]
	print(history_lst)
	print("Now, enter the number of a recipe you'd like to try.")
	idea = input()
	rating = itemitemcollab(idea,history_lst,5)
	print("Your expected rating for "+ recipe_names[idea] + " is ", rating)
	if rating > 4:
		print("It seems like you would love this recipe!")
	elif rating > 3:
		print("You might like this recipe.")
	else:
		print("You might want to keep looking :/")

else:
	print("How many recipes would you like to add to your recipe history?")
	history_length = int(input())
	history_lst = [0]*history_length

	for i in range(history_length):
		outpt = []
		if i == 0:
			print("Great! What kind of recipe would you like to enter? Enter one or more space-separated keywords:")
		else:
			print("Added! Pick another recipe. Enter one or more space-separated keywords:")
		keywords = input().split(" ")
		for word in keywords:
			# print("word is: ", word)
			# print(recipe_dict.keys())
			outpt.extend([(recipe_namesrev[s],s) for s in recipe_namesrev.keys() if word in s.lower()])
		print(outpt)
		print("Pick one recipe from the selection above by entering the recipe number.")
		history_lst[i] = int(input())

	# history_lst = [int(x) for x in indices.split(" ")]
	# print(history_lst)


	user_list = [create_user() for i in range(20)]
	# print(user_list)
	for user in user_list:
		userprofile(user)

	user_profile = [0]*profile_length
	for index in history_lst:
		recipe_profile = recipe_dict[recipe_list[index]]['profile']
		for i in range(profile_length):
			user_profile[i] += recipe_profile[i]

	user_profile = [x/profile_length for x in user_profile]

	print("Content Recommendation: ", contentrecommend(user_profile))
	print(useruser(user_profile, user_list))
