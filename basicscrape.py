from recipe_scrapers import scrape_me

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

def read_data():
	f = open("rec1.txt",'r')
	recipes = []

	for link in f:
		if link[0:34] == "https://www.allrecipes.com/recipe/":
			recipes.append(link)

	num_recipes = len(recipes)

	i = 0

	for recipe in recipes[:10]:

		scraper = scrape_me(recipe.rstrip())
		servings = int(scraper.yields()[0])
		title = scraper.title()
		recipe_dict[title] = {'time':scraper.total_time(), 'yields': servings, 'ingredients': scraper.ingredients(), 'instructions': scraper.instructions(), 'profile': [0,0,0,0,0,0]}
		recipe_names[i] = title
		recipe_list.append(title)
		# content profile about recipes' length -- index 0
		if recipe_dict[scraper.title()]['time'] < 30:
			recipe_dict[scraper.title()]['profile'][0] = 0.3
		elif recipe_dict[scraper.title()]['time'] < 80:
			recipe_dict[scraper.title()]['profile'][0] = 0.6
		else:
			recipe_dict[scraper.title()]['profile'][0] = 0.9

		# recipe yield attribute -- index 1
		if recipe_dict[scraper.title()]['yields'] < 4:
			recipe_dict[scraper.title()]['profile'][1] = 0.2
		elif recipe_dict[scraper.title()]['time'] < 6:
			recipe_dict[scraper.title()]['profile'][1] = 0.4
		elif recipe_dict[scraper.title()]['time'] < 8:
			recipe_dict[scraper.title()]['profile'][1] = 0.6
		else:
			recipe_dict[scraper.title()]['profile'][1] = 0.9

		# sweetness attribute -- index 2
		for ingredient in recipe_dict[scraper.title()]['ingredients']:
			if (ingredient.find('sugar') != -1) or (ingredient.find('chocolate') != -1):
				recipe_dict[scraper.title()]['profile'][2] = 1

		# spiciness attribute -- index 3
		for ingredient in recipe_dict[scraper.title()]['ingredients']:
			if (ingredient.find('pepper') != -1) or (ingredient.find('spicy') != -1) or (ingredient.find('chili') != -1):
				recipe_dict[scraper.title()]['profile'][3] = 1

		# baking attribute -- index 4
		if (recipe_dict[scraper.title()]['instructions'].find('bake') != -1) or (recipe_dict[scraper.title()]['instructions'].find('Bake') != -1): 
			recipe_dict[scraper.title()]['profile'][4] = 1

		i += 1
		# to use later if necessary:
		#'image': scraper.image()
		#'links': scraper.links()

	return recipe_dict, recipe_names, recipe_list

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

read_data()
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

