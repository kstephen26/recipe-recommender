# very basic user class
import random

class User:
    def __init__(self, favorites, idf):
        self.id = idf
        self.favorites = favorites
        self.reciperatings = dict([(x, random.randint(1,5)) for x in self.favorites])
        # self.reciperatings = {x:  for (key, value) in iterable}
        self.profile = []
        self.type = ''
    
    def add_favorite(self, recipe):
        self.favorites.append(recipe)

    def getratings(self):
        self.reciperatings = [(x, random.randint(1,5)) for x in self.favorites]
        return self.reciperatings

