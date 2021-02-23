#!/usr/bin/python
import re
import sys

filename = sys.argv[1]
if "/" in filename:
    rindex = filename.rindex("/")
    generated_filename = filename[rindex+1:-3]+".html"
else:
    generated_filename = filename[:-3]+".html"

frags = [
#       replace this        with this
    ['%container%','<div class="container">' ],
    ['%directions%','<div class="directions">' ],
    ['%ingredients%','<div class="ingredients">'],
    ['%sidebyside%','<div class="sidebyside">'],
    ['%enddiv%','</div>'],
    ['%noprint%','<div class="noprint">'],
    ['%header%', '<div class="header">'],
    ['%generated_filename%', generated_filename],
    ['%base_filename%', generated_filename[:-5]+".md"],
]

if "index" in filename:
    frags.append(['%up%', 'https://githubrecipes.com'])
else:
    frags.append(['%up%', 'index.html'])

with open('footer.md', 'r') as f:
    footer = f.read()
    for item in frags:
        footer = footer.replace(item[0], item[1])
frags.append(['%footer%', footer])

#get metadata tags
metadata_pat = r'^(.*?): (.*?)$'
with open(filename, 'r') as f:
    data = f.read()
    for line in data.split("\n"):
        if line=="...\n":
            break
        match = re.match(metadata_pat, line)
        if match:
            var_name = "%"+match.group(1)+"%"
            var_val = match.group(2)
            frags.append([var_name, var_val])

    for item in frags:
        data = data.replace(item[0], item[1])

# output to stdin to pandoc
print(data)




