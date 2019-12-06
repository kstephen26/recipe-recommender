from recipe_scrapers import scrape_me
import ast
import json
import random
from random import seed
from user import User
recipe_dict = json.load(open("recipe_dict.txt"))
recipe_names = json.load(open("recipe_names.txt"))
recipe_namesrev = {}
for number in recipe_names:
	recipe_namesrev[recipe_names[number]] = number
# print(recipe_namesrev)

recipe_list = list(recipe_dict.keys())

def create_user():
	user_history = []
	for i in range(100):
		k = random.randint(1,359)
		user_history.append(recipe_names[str(k)])
	new_user = User(user_history,1)
	return new_user

def create_smart_user(keyword, idf):
	p = 0.9
	user_history = []
	for recipe in recipe_names:
		j = random.random()
		if j < 0.6:
		# j is so that we don't end up adding every single recipe
			name = recipe_names[recipe]
			k = random.random()
			if keyword in name.lower() or keyword in recipe_dict[name]['ingredients'] or keyword in recipe_dict[name]['instructions']:
				if k < p:
					user_history.append(name)
				else:
					l = random.randint(1,359)
					user_history.append(recipe_names[str(l)])
			elif j < 0.01:
				l = random.randint(1,359)
				user_history.append(recipe_names[str(l)])

	new_user = User(user_history,idf)
	new_user.type = keyword
	return new_user


smart_user_list = []
smart_user_list.extend([create_smart_user('indian',i) for i in range(1,5)])
smart_user_list.extend([create_smart_user('thai',i) for i in range(5,9)])
smart_user_list.extend([create_smart_user('italian',i) for i in range(9,13)])
smart_user_list.extend([create_smart_user('cake',i) for i in range(13,17)])
smart_user_list.extend([create_smart_user('easy',i) for i in range(17,21)])
smart_user_list.extend([create_smart_user('cookies',i) for i in range(21,25)])

# with open('smartusers.txt', 'w') as f:
#     for user in user_list:
#         f.write('%s\n' % user)

# nulist = []

# with open('smartusers.txt', 'r') as f:
#     nulist = [x.rstrip() for x in f.readlines()]

# for user in nulist:
# 	print("User type is: ", user.type)
# 	print("User recipes are: ", user.favorites)

