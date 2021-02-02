# raid_the_fridge

https://spoonacular.com/food-api

This app is deployed at raidthefridge.herokuapp.com.

The website uses the spoonacular food api to pull requests for recipes. There are three options on the app, the first is a search option which allows the user to enter food that they currently have and find out what recipes can be made from it. for instance a user could type "chicken, broccoli" and get recipes that include chicken and broccoli. if words are misspelled an error is flashed to encourage users to correct their spelling and ensure that each ingredient is separated by a comma. The page displays 10 recipes.

The second way to search is random. On each refresh the page loads 10 new recipes that are completely random, be they desserts, drinks, dinners, sandwiches etc. On each recipe there is a button to add to a favorites page titled "My Recipes" A user is asked to log in and their recipes are saved to a postgresql database. on the my recipe page there is an option to delete a recipe from the list.

##About the API##

The spoonacular API is pretty large. they boast over 300,000 recipes. The downsides that I've noticed are that the same 10 recipes show up for each search. For example if I searched for chicken 5 times, I would get the same 10 chicken recipes 5 times. Also some of the recipes don't have an image attached to them so it makes the website look a bit novice. also on the random recipe generator I notice that the same recipes are often re-used. 

##The Stack##

The site was created using Python, Flask, HTML5, CSS3, PostgreSQL, and SQLAlchemy primarily.
