# very basic user class
class User:
    def __init__(self, favorites):
        self.favorites = favorites
        self.profile = []
    
    def add_favorite(self, recipe):
        self.favorites.append(recipe)
