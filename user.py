# very basic user class
class User:
    def __init__(self, name):
        self.name = name
        self.favorites = []
    
    def add_favorite(self, recipe):
        self.favorites.append(recipe)
