from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
scraper = scrape_me('https://www.allrecipes.com/recipe/220996/easy-homemade-pie-crust/')

x = scraper.title()
scraper.total_time()
scraper.yields()
scraper.ingredients()
scraper.instructions()
scraper.image()
scraper.links()

print(x)