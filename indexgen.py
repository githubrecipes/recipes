import re
from os import walk
import os

#run in the base directory
ignore_dirs = [".github", ".git"]
author_pat = r'author: (.*?)\n'
title_pat = r'title: (.*?)\n'
prep_pat = r'prep: (.*?)\n'
cook_pat = r'cook: (.*?)\n'

def as_html(md_file):
    return md_file[:-3]+".html"

def header(title):
    md_file = ""
    md_file += "---\n"
    md_file += "title: "+title+"\n"
    md_file += "...\n"
    md_file += "<!-- AUTOGENERATED DO NOT ALTER -->\n"
    return md_file


dirs = {}
for (dirpath, dirnames, filenames) in walk(os.getcwd()):
    folder_name = dirpath[dirpath.rindex("/")+1:]
    if ".github" in dirpath or ".git" in dirpath or folder_name=="recipes":
        continue
    dirs[folder_name] = 0

    print("Generating index:", folder_name)
    md_file = header(folder_name.title())
    md_file += "| Title | Prep Time | Cook Time | Author |\n"
    md_file += "| :---: | :-------: | :-------: | :----: |\n"
    md_path = dirpath+"/index.md"
    for file in filenames:
        if ".md" in file and not "index" in file:
            dirs[folder_name] += 1
            with open(dirpath+"/"+file, 'r') as f:
                fcontents = f.read()
                author_match = re.findall(author_pat, fcontents)
                title_match = re.findall(title_pat, fcontents)
                prep_match = re.findall(prep_pat, fcontents)
                cook_match = re.findall(cook_pat, fcontents)
                author = author_match[0] if author_match else "anon";
                title = title_match[0] if title_match else file;
                prep = prep_match[0] if prep_match else "???";
                cook = cook_match[0] if cook_match else "???";

            print(author, title, prep, cook)
            md_file+="| ["+title+"]("+as_html(file)+") | "+prep+" | "+cook+" | "+author+" |\n"
    md_file += "%footer%\n"
    print(md_file)
    with open(md_path, 'w') as out_file:
        out_file.write(md_file)



md_file = header("Github Recipes")
md_file += "# %title%\n"
md_file += "## Categories\n"
md_file += "| Category | Number of Recipes | PDF |\n"
md_file += "| :------: | :---------------: | :-: |\n"
sorted_dirs = {v: dirs[v] for v in sorted(dirs)}
print(dirs, sorted_dirs)
for key, value in sorted_dirs.items():
    if value!=0:
        md_file += "| [{}]({}) | {} | N/A |\n".format(key.title(), key+"/index.html", value)
        print(key,value)

md_file += "%footer%"
print(md_file)

with open("index.md", 'w') as f:
    f.write(md_file)



