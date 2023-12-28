# CS50-CookApp-Final-Project
Cook App is an app which helps you plan your meals ahead. 
Android app made using Python kivy and kivymd framework.
### Made by Kinga Tkocz as a final project for CS50 Computer Science course
#### Video description: https://youtu.be/zAbmxHon9aI


## There are two main features

### Saving recipes
First one is saving your recipes so you can find them any time
you need. You can do that by hitting Recipes -> + Button (at the bottom of your screen), after that new screen will pop up
and you will be able to write the name for your recipe, insert needed ingredients and write
cooking steps. There is also an option to upload your custom photo for your recipe but in order
to do that be sure to give Cook App access to your files and I also recommend adding new folder (album) 
to your gallery since default file manager may struggle loading a lot of photos at the same time.
When your satisfied with what you entered you need to click a save button then click upper left corner button 
to go back to search screen and you should be able to see your new recipe added to the list. There is
also search option so if you have many recipes, it will be easier to find the one you are
looking for.

### Creating shopping list
Second one is creating your shopping list. You can do that by hitting Lists -> + Button (at the bottom of your screen),
after that you will be prompted to add new item and the quantity of it. If you add two items with the same
name they will show quantity separated by "," instead of creating another entry. There is also
option to automatically add ingredients which you need for particular recipe via add buttons on
recipe tile or in the right upper corner when you click on specific recipe tile.


## Issues I faced during development
It was my first time I have been using kivy framework so it showed me how important is good documentation for programming tools
since I had to read it a lot. Also, it was my first own project in which I used object-oriented programming. The biggest challenge
for me was to actually build my app with buildozer since I had to use VirtualBox with Linux, download a lot of packages with needed 
tools and to solve problems with file picker and hiding input field but I finally did it and I am proud of my work. I hope you will
find my app useful.
