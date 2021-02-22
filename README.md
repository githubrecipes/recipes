# GithubRecipe repository

Open a PR with your own correctly formatted recipe markdown files and it will be pushed to the website pending approval.

## Philosophy

- No fluff
    + If you feel compelled to add something extraneous to the recipe keep it within the `noprint` section.
- Unambiguous directions
    + This is hard to define but you know it when you see it
    + The directions should be step by step
        * Assume reader has **basic** cooking skills
            - In practice this means if I have done it before it doesn't need to be explained. 
- One page print is a priority
    + This is hard to judge but a good rule of thumb is keep your recipe and ingredient list together below around 50-60 lines.

## Style guide
### Ingredient List
Use the markdown table format as seen in the `template.md` file.

+ Approved unit abbreviations
    * `Tablespoon -> table`
    * `Teaspoon -> tea`
    * `Pounds -> lbs`
+ For items like vegetables/fruits; use \[1-4\]x format.
+ Use units that can be inferred from packaging;
+ Avoid unit conversion from those listed on packaging
    * Americans find imperial units as confusing as everyone else.
    * Don't ask for lbs when packages has the quantity listed in oz.
+ Use fractions over decimals
    * 1/2 cup not 0.5 cups

### Directions
Use numbered lists for directions either manually (1., 2., etc) or with pandoc syntax ((@), (@), etc.).
+ If a direction uses multiple ingredients note each one on a separate sub-bullet like;
+ Mix
    * Onions
    * Cheese
    * Etc.
+ If a direction 
+ For temperatures default to Fahrenheit temperatures
    * Bold all preheating instructions
    * Bold temperatures and cooking times using the double asterik (\*\**)
        * Eg: Cook at **350F** for **4 hours**

### Metadata
These metadata tags are used to generate the index pages for each subdirectory. It is important they are included at the top of the file in the same format laid out in the template and below!!!

Only the first four are required. The rest are not currently used but maybe in the future.
```
---
author: <persons name>
title: <the title to be used on the index page>
prep: <prep time for the recipe>
cook: <cook time for the recipe>
serves: <how many servings recommended amounts creates>
cal: <calories for recipe>
socialmedia: <link to be included if twitter intergration is implemented>
credit: <link to adapted recipe>
bake: <bake time (set and forget til timer)>
...
```
Note that there has to be a space after the colon (:)
You can use the defined metadata (`%title%` will be replace with whatever the contents of the variable is) later on in the file like shown in `applepie.md`.

The replacement is a bit fussy;

`Prep: %prep%` works while `Prep:%prep%` does not

## Writing your own
1. Create a [new file](https://github.com/githubrecipes/recipes/new/main)
2. At the top of the page select the most appropriate folder and the name of the file.
    - The filename should be descriptive while short.
3. Copy the [template](https://raw.githubusercontent.com/githubrecipes/recipes/main/template.md) into the file
4. Starting editing! Using the above style guide!
5. Once you are satisfied (don't worry you can edit it later) scroll to the bottom of the page and Select 

    `Create a new branch for this commit and start a pull request`.
6. Click `Propose new file`!
7. Wait patiently for the PR to be approved

You can also edit the file locally if you don't like the github editor. 

If you want to preview how the file is going to look when published check out the [`Development`](#Development) section below.

You can create your own folder and file using the github.com interface. Only create your own folder if your recipe doesn't fall into the other categories.

**Anything** that is not the ingredient list or direction list **must** be inside the `<div class="noprint">` which **must** be found at the bottom of the file. As you may have guessed from the class name, anything found in this section of the page will not show up when the user goes to print the recipe.

## Legality

If you are adapting a recipe from one found online or in a cookbook/ on packaging **you must** include the original source it was adapted/inspired by.

From [copyright.gov's circular 33](https://www.copyright.gov/circs/circ33.pdf):
```
A recipe is a statement of the ingredients and procedure required for making a dish of food. A mere
listing of ingredients or contents, or a simple set of directions, is uncopyrightable.
```

The important part is the qualification of "simple". If the original recipe contains in depth instruction about a unique cooking technique it does not belong in this repo. The core idea behind this project is one page dead simple recipes.


## Your style guide is dumb/makes no sense
Open a PR/issue suggesting changes and reasons why.


## Development
To build the website locally:
1. Clone this repo
    
    `git clone https://github.com/githubrecipes/recipes.git`
2. Install [`pandoc`](https://pandoc.org/installing.html)
3. If you use [sublime text 3](https://www.sublimetext.com/3) you can open the folder as a project and just build (`Ctrl+b`) individual files.
4. To build the file you're working on locally;
    
    `pandoc -s --css=styling.css --to=html5 <input_file> -o <output_file>`
5. Open the file in your web browser of choice.

Be sure that the repo is up-to-date as it will be using the local version of the CSS file.

## CSS source
CSS has been adapted from [Pan Am: *Simple CSS for Pandoc*](https://benjam.info/panam/)

You can open a PR in this Repo if you have any changes/suggestions for the CSS used by the website.

I'll eventually add something that minimizes the CSS in the github action before committing to pages repo.

## TODO
1. Minimize CSS for committing to pages repo
2. Favicon/icon for github recipes
3. Github action to build PR files so people can preview what it will look like
4. Metadata system
5. Twitter posting when new item added.
6. Main index page
7. Titles on index pages!
8. Back links
9. "up in the file tree" links
    IE clicking this on the pecan pie page brings you back to desserts
10. View source function on each web page
