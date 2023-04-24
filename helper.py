from bs4 import BeautifulSoup
import requests

class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = {}

    def __str__(self):
        return self.name
  
def parseIngredients(recipe, ingredients):
    ingredients_list = ingredients.split()
    ingredients_list = ingredients_list[::-1]
    while (len(ingredients_list) > 0):
        if ingredients_list[0][1].isnumeric():
            quant = ingredients_list.pop(0).strip('()')
            ingredient = ingredients_list.pop(0)
            while (len(ingredients_list) > 0 and not ingredients_list[0][1].isnumeric()):
                if ingredients_list[0] == '(Any)':
                    ingredients_list.pop(0)
                else:
                    ingredient = ingredients_list.pop(0) + ' ' + ingredient
        recipe.ingredients[ingredient] = quant
  
page_to_scrape = requests.get('https://stardewvalleywiki.com/Cooking')
soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
recipe_header = soup.find('h2', string='Recipes')
recipes_html = recipe_header.findNext('table')
headers_html = recipes_html.findAll('tr')[0].findAll('th')
headers = []
for header in headers_html:
    headers.append(header.text)

def get_recipes_and_ingredients():
    recipes = []
    for row in recipes_html.find('tbody').children:
        if len(list(row)) > 1:
            data = row.findAll('td')
            if len(data) > 1:
                recipe = Recipe(data[headers.index('Name')].text.rstrip('\n'))
                recipes.append(recipe)
                parseIngredients(recipe, data[headers.index('Ingredients')].text)
    recipes_massaged = []
    for recipe in recipes:
        for item in list(recipe.ingredients):
            recipes_massaged.append([recipe.name, item, recipe.ingredients[item]])
    return recipes_massaged