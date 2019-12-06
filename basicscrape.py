from recipe_scrapers import scrape_me
import ast
import json
import random
import smartusers
from user import User
import numpy as np

# give the url as a string, it can be url from any site listed below

profile_length = 8
recipe_dict = {}
recipe_names = {}
recipe_list = []
recipe_dict = json.load(open("recipe_dict.txt"))
recipe_names = json.load(open("recipe_names.txt"))
recipe_namesrev = {}
itemitemhistory = []
for number in recipe_names:
	recipe_namesrev[recipe_names[number]] = number
recipe_list = list(recipe_dict.keys())

# Cosine similarity scores of two user/recipe profiles
def cosine_sim(l1, l2):
	if len(l1) != len(l2):
		return None
	d1 = (sum([x*x for x in l1]))**0.5
	d2 = (sum([x*x for x in l2]))**0.5
	n1 = 0
	for i in range(len(l1)):
		n1 += l1[i]*l2[i]
	return n1/(d1*d2)

# Generates an average of a user's recipe profiles to numerically represent their aggregated preferences
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

# Content-based recommendation. First option is the given recipe.
# Returns the top four recommendations based on cosine similarity
def contentrecommend(userprof):
	maxsim = 0
	maxrecipe = "hello"
	reclist = []
	for recipe in recipe_dict.keys():
		profile = recipe_dict[recipe]['profile']
		sim = cosine_sim(userprof, profile)
		reclist.append([recipe,sim])
	reclist = sorted(reclist, key=lambda lst: lst[1], reverse = True)
	reclist = [x[0] for x in reclist]
	return reclist[:4]

# Content-based rating of a given recipe (out of 5 stars). First option is the given recipe.
def contentrate(userprof, idea):
	return round(5*cosine_sim(userprof, recipe_dict[recipe_names[str(idea)]]['profile']))

# Item-item collaborative filtering, rating a given recipe out of 5 stars based on a user's history
def itemitemcollab(idea, history, k):
	# idea is the index of a recipe idea, history is the list of index and rating tuples of recipes cooked in the past. k is neighborhood size.
	#print("idea ", idea)
	#print("history", history)
	global itemitemhistory
	reclist = []
	userprof = recipe_dict[recipe_names[idea]]['profile']
	#print("history is "), itemitemhistory
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
	
# User-user collaborative filtering, generating a novel recommendation based on user and peer profiles
def useruser(userprof,peer_list):
	similar_peers = []
	k = 5
	for peer in peer_list:
		sim = cosine_sim(userprof, peer.profile)
		similar_peers.append([sim, peer])
	similar_peers = sorted(similar_peers, key=lambda lst: lst[0], reverse = True)
	compiled_recipes = {}
	for i in range(k):
		sim, peer = similar_peers[i]
		peer_recipes = peer.favorites
		for recipe in peer_recipes:
			if recipe in compiled_recipes:
				compiled_recipes[recipe] += 1
			else:
				compiled_recipes[recipe] = 1
	return max(compiled_recipes, key=compiled_recipes.get)

# Uses user-user collorative filtering to generate a rating (out of 5 stars) for a given "idea" recipe
def useruserrate(idea, userprof, peer_list):
	similar_peers = []
	k = 5
	for peer in peer_list:
		sim = cosine_sim(userprof, peer.profile)
		similar_peers.append([sim, peer])
	similar_peers = sorted(similar_peers, key=lambda lst: lst[0], reverse = True)
	num = 0
	denom = 0
	if int(idea) > 359:
		return "Idea not in recipe database"
	targetrec = recipe_names[idea]
	for i in range(k):
		peer = similar_peers[i][1]
		if targetrec in peer.reciperatings:
			num += similar_peers[i][0]*peer.reciperatings[targetrec]
			denom += abs(similar_peers[i][0])
	if denom == 0:
		return None
	else:
		return num/denom

# Creates a simple user with a randomized history
def create_user():
	user_history = []
	for i in range(100):
		k = random.randint(1,359)
		user_history.append(recipe_names[str(k)])
	new_user = User(user_history,1)
	return new_user

def makematrix(userlist):
	maxid = max([user.id for user in userlist])
	reclen = len(recipe_list)
	userlen = len(userlist)
	outpt = [ ([0] * reclen) for row in range(maxid) ]
	# outpt = [[0]*reclen]*maxid
	# print(outpt)
	# for i in range(userlen):
	# 	for j in recipe_names:
	# 		if 
	# 		outpt[i][j] = 
	for user in userlist:
		# print("user id: ", user.id)
		for j in recipe_names:
			if recipe_names[j] in user.favorites:
				# print(user.id)
				# print((user.id - 1, int(j)))
				outpt[user.id - 1][int(j)] = user.reciperatings[recipe_names[j]]
		# print(outpt)
	return outpt

# print(recipe_dict)
# print(recipe_names)
# print(recipe_list)
# print("Available Selection:", recipe_names)
# print("Select a recipe history using recipe indices above:")
# indices = input()

# system_type = 'Item-Item'
system_type = 'Matrix Factorization'

def print_recipes_index():
	dict_keys = list(recipe_names.keys())
	dict_keys.sort(key = lambda x: int(x))
	for num in dict_keys:
		print(int(num), ": ",recipe_names[num])

print("Enter 'recommend' if you would like to be recommended a new recipe or 'rate' if you would like a predicted rating on a recipe idea.")
option = input()
if option == 'recommend':

		print("What type of recommender would you like ('collaborative' or 'contentbased'): ")
		system_type = input()

		if system_type == 'contentbased':

			print_recipes_index()
			print("How many recipes would you like to add to your recipe history?")
			history_length = int(input())
			history_lst = [0]*history_length

			for i in range(history_length):
				outpt = []
				if i == 0:
					print("Great! What kind of recipe would you like to enter? Enter one or more space-separated keywords:")
				else:
					print("Added! Pick another recipe. Enter one or more space-separated keywords:")
				keywords = input().strip().split(" ")
				for word in keywords:
					outpt.extend([(recipe_namesrev[s],s) for s in recipe_namesrev.keys() if word in s.lower()])
				print(outpt)
				print("Pick one recipe from the selection above by entering the recipe number.")
				history_lst[i] = int(input())

			user_profile = [0]*profile_length
			for current_recipe_name in history_lst:
				recipe_profile = recipe_dict[recipe_names[str(current_recipe_name)]]['profile']
				for i in range(profile_length):
					user_profile[i] += recipe_profile[i]
			user_profile = [x/profile_length for x in user_profile]

			print("Top 5 Recommended Recipes:",contentrecommend(user_profile))

		elif system_type == 'collaborative':
			print_recipes_index()
			print("Enter numeric keys for your favorite recipes, space-separated:")
			history_nums_lst = input().strip().split()
			history_lst = [recipe_names[num] for num in history_nums_lst]
			#print(history_lst)
			## Creating dummy user profiles
			user_list = [create_user() for i in range(20)]
			# print(user_list)
			for user in user_list:
				userprofile(user)

			user_profile = [0]*profile_length
			for current_recipe_name in history_lst:
				recipe_profile = recipe_dict[current_recipe_name]['profile']
				for i in range(profile_length):
					user_profile[i] += recipe_profile[i]
			user_profile = [x/profile_length for x in user_profile]
			rec_recipe = useruser(user_profile, user_list)
			print("Recommended Recipe:",rec_recipe)
			cos_sim = cosine_sim(user_profile, recipe_dict[rec_recipe]['profile'])
			print("Similarity: ", cos_sim)

		else:
			print("You'll have to run this program again and enter a string corresponding to the system you'd like to select.")

if option == 'rate':

	print("What type of rater would you like ('itemitem', 'useruser', 'contentbased', or 'hybrid'): ")
	system_type = input()
	systemlist = ['itemitem', 'useruser', 'contentbased', 'hybrid']

	if system_type not in systemlist:
		print("You'll have to run this program again and enter a string corresponding to the system you'd like to select.")

	if system_type == 'hybrid':
		alpha = 0.3333
		beta = 0.3333
		gamma = 0.3333
		eta = 0.1
		print("How many games do you want to play?")
		iters = int(input())
		while iters > 0:
			iters -= 1
			history_length = 0
			while history_length < 5:
				print("How many recipes would you like to add to your recipe history (at least 5)?")
				history_length = int(input())
				if history_length < 5:
					print("Recipe history size too small. Let's try again.")
			print_recipes_index()
			history_lst = [[0,0]]*history_length
			for i in range(history_length):
				print("Enter a recipe number and rating (1-5) from the above selection separated by a space.")
				currhistory = [int(x) for x in input().strip().split(" ")]
				if len(currhistory) != 2 or currhistory[0] > 359 or currhistory[0] < 0 or currhistory[1] > 5 or currhistory[1] < 0:
					print('The recipe or rating you have submitted is invalid. Try again.')	
					i -= 1	
				else:
					history_lst[i] = currhistory	
			print("Your inputted recipe names: rating'")
			for item in history_lst:
				print(recipe_names[str(item[0])]+": "+str(item[1]))

			print("Now, enter the number of a recipe you'd like to try.")
			idea = input()

			## Creating dummy user profiles
			user_list = [create_user() for i in range(50)]
			# print(user_list)
			for user in user_list:
				userprofile(user)

			user_profile = [0]*profile_length
			for current_recipe_name, rating in history_lst:
				recipe_profile = recipe_dict[recipe_names[str(current_recipe_name)]]['profile']
				for i in range(profile_length):
					user_profile[i] += recipe_profile[i]
			user_profile = [x/profile_length for x in user_profile]

			urating = useruserrate(idea, user_profile, user_list)
			# print("urating is ", urating)
			irating = itemitemcollab(idea, history_lst, 5)
			crating = contentrate(user_profile, idea)
			if urating == None:
				rating = 0.5*irating + 0.5*crating
			else:
				rating = min(alpha*urating + beta*irating + gamma*crating,5)

			print("Your expected rating for "+ recipe_names[idea] + " is ", rating)
			if rating > 4:
				print("It seems like you would love this recipe!")
			print("-------------------------------------")
			print("Nice job cooking! What was your actual rating for this recipe?")
			actualrating = int(input())

			# Learning Sequence. Increases the user-specific weight of ratings that were more accurate to the user's actual rating.
			if actualrating != urating and urating != None:
				alpha = min(alpha*eta/(actualrating - urating),0.8)
				# print(alpha)
			if actualrating != crating and urating != None:
				beta = min(beta*eta/(actualrating - crating),0.8)
				# print(beta)
			if actualrating != irating and urating != None:
				gamma = min(gamma*eta/(actualrating - irating),0.8)
				# print(gamma)

			rawweights = [alpha, beta, gamma]
			normedweights = [i/sum(rawweights) for i in rawweights]
			# print(normedweights)
	else: 
		# single iteration games

		history_length = 0
		while history_length < 5:
			print("How many recipes would you like to add to your recipe history (at least 5)?")
			history_length = int(input())
			if history_length < 5:
				print("Recipe history size too small. Let's try again.")
		print_recipes_index()
		history_lst = [[0,0]]*history_length
		for i in range(history_length):
			print("Enter a recipe number and rating (1-5) from the above selection separated by a space.")
			currhistory = [int(x) for x in input().strip().split(" ")]
			if len(currhistory) != 2 or currhistory[0] > 359 or currhistory[0] < 0 or currhistory[1] > 5 or currhistory[1] < 0:
				print('The recipe or rating you have submitted is invalid. Try again.')	
				i -= 1	
			else:
				history_lst[i] = currhistory
		print("Your inputted recipe names: rating'")
		for item in history_lst:
			print(recipe_names[str(item[0])]+": "+str(item[1]))

		print("Now, enter the number of a recipe you'd like to try.")
		idea = input()
		user_profile = [0]*profile_length
		for current_recipe_name, rating in history_lst:
			recipe_profile = recipe_dict[recipe_names[str(current_recipe_name)]]['profile']
			for i in range(profile_length):
				user_profile[i] += recipe_profile[i]
		user_profile = [x/profile_length for x in user_profile]

		if system_type == 'contentbased':
			
			rating = contentrate(user_profile, idea)

		elif system_type == 'itemitem':

			rating = itemitemcollab(idea, history_lst, 5)

		elif system_type == 'useruser':
			## Creating dummy user profiles
			user_list = [create_user() for i in range(50)]
			# print(user_list)
			for user in user_list:
				userprofile(user)

			rating = useruserrate(idea, user_profile, user_list)

		elif system_type == 'Matrix Factorization':

			actuallist = [x[0] for x in history_lst]
			ouruser = User(actuallist,25)
			ouruser.reciperatings = dict(history_lst)

			user_list = smartusers.smart_user_list
			user_list.append(ouruser)
			matrx = makematrix(user_list)
			QR = np.linalg.qr(matrx)
			# print(QR[0].shape)
			Q = QR[0]
			R = QR[1]
			Rt = np.transpose(R)
			# print(QR[1].shape)
			rating = np.dot(Q[-1],Rt[idea])

		print("Your expected rating for "+ recipe_names[idea] + " is ", rating)
		if rating > 4:
			print("It seems like you would love this recipe!")
		elif rating > 3:
			print("You might like this recipe.")
		else:
			print("You might want to keep looking :/")