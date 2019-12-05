from recipe_scrapers import scrape_me
import ast
import json

profile_length = 8
recipe_dict = {}
recipe_names = {}
recipe_list = []

def read_data():
	f = open("rec1.txt",'r')
	recipes = []

	for link in f:
		if link[0:34] == "https://www.allrecipes.com/recipe/":
			recipes.append(link)

	num_recipes = len(recipes)

	i = 0

	#for recipe in recipes:
	for x in range(200, 210):
		recipe = recipes[x]
		scraper = scrape_me(recipe.rstrip())
		title = scraper.title()

		if title not in recipe_dict:

			servings = int(scraper.yields().split()[0])
			print(servings)
			
			recipe_dict[title] = {'time':scraper.total_time(), 'yields': servings, 'ingredients': scraper.ingredients(), 'instructions': scraper.instructions(), 'profile': [0 for _ in range(profile_length)]}
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
			elif recipe_dict[scraper.title()]['yields'] < 6:
				recipe_dict[scraper.title()]['profile'][1] = 0.4
			elif recipe_dict[scraper.title()]['yields'] < 8:
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

			# dairy attribute -- index 5
			for ingredient in recipe_dict[scraper.title()]['ingredients']:
				if (ingredient.find('milk') != -1) or (ingredient.find('butter') != -1) or (ingredient.find('cheese') != -1) or (ingredient.find('cream') != -1):
					recipe_dict[scraper.title()]['profile'][5] = 1
			
			# meat attribute -- index 6
			for ingredient in recipe_dict[scraper.title()]['ingredients']:
				if (ingredient.find('meat') != -1) or (ingredient.find('beef') != -1) or (ingredient.find('chicken') != -1) or (ingredient.find('pork') != -1) or (ingredient.find('veal') != -1) or (ingredient.find('lamb') != -1) or (ingredient.find('fish') != -1) or (ingredient.find('turkey') != -1) or (ingredient.find('bacon') != -1) or (ingredient.find('duck') != -1):
					recipe_dict[scraper.title()]['profile'][6] = 1
			
			# Nut allergies attribute --  index 7 (including just "nut" triggers false positives on foods like "butternut squash")
			for ingredient in recipe_dict[scraper.title()]['ingredients']:
				if (ingredient.find('peanut') != -1) or (ingredient.find('walnut') != -1) or (ingredient.find('pecan') != -1) or (ingredient.find('almond') != -1) or (ingredient.find('cashew') != -1) or (ingredient.find('pistachio') != -1):
					recipe_dict[scraper.title()]['profile'][7] = 1

			print(recipe_dict[scraper.title()]['profile'])
			i += 1
			# to use later if necessary:
			#'image': scraper.image()
			#'links': scraper.links()

def write_dict(dictionary, file):
	json.dump(dictionary, open(file,'w'))

read_data()
write_dict(recipe_dict, 'recipe_dict.txt')
write_dict(recipe_names, 'recipe_names.txt')