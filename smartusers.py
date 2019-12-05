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
	new_user = User(user_history)
	return new_user

def create_smart_user(keyword):
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

	new_user = User(user_history)
	new_user.type = keyword
	return new_user

user_list = []
user_list.extend([create_smart_user('indian') for i in range(3)])
user_list.extend([create_smart_user('thai') for i in range(3)])
user_list.extend([create_smart_user('italian') for i in range(3)])
user_list.extend([create_smart_user('cake') for i in range(3)])
user_list.extend([create_smart_user('easy') for i in range(3)])
user_list.extend([create_smart_user('cookies') for i in range(3)])

for user in user_list:
	print("User type is: ", user.type)
	print("User recipes are: ", user.favorites)

