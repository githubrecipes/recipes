#!/usr/bin/python
import re
import sys
import json
import argparse

def replacement(match):
    return frags["%"+match.group(1)+"%"]*int(match.group(2))


parser = argparse.ArgumentParser(description="HTML grep tool")

parser.add_argument('-f', '--frags', dest="fragment_file", action="store", default="frags.json", help="Path to frag file for find and replace")
parser.add_argument('input', action="store", help="Input file to match and replace")
parser.add_argument("-o", "--output", dest="output", action="store", help="Output file to save results to. Default is stdout")

args = parser.parse_args()

filename = args.input

if "/" in filename:
    rindex = filename.rindex("/")
    generated_filename = filename[rindex+1:-3]+".html"
else:
    generated_filename = filename[:-3]+".html"

# load in all of the frags
frags = {}
files = []
with open(args.fragment_file, 'r') as f:
    data = json.loads(f.read())
    for item in data:
        name = '%'+item+'%'
        content = data[item]

        if type(content) is list:
            if content[0] == "file_content":
                with open(content[1], 'r') as fc:
                    frags[name] = fc.read()
                    files.append(name)
            elif content[0] == "input_file_name":
                frags[name] = filename
            elif content[0] == "output_file_name":
                frags[name] = generated_filename
        else:
            frags[name] = content

for file in files:
    data = frags[file]
    for item in frags:
        data = data.replace(item, frags[item])
    frags[file] = data

if "index" in filename:
    frags['%up%'] = 'https://githubrecipes.com'
else:
    frags['%up%'] = 'index.html'

#get metadata tags
metadata_pat = r'^(.*?):(.*?)$'
with open(filename, 'r') as f:
    data = f.read()
    for line in data.split("\n"):
        if line=="...":
            break
        match = re.match(metadata_pat, line)
        if match:
            var_name = "%"+match.group(1)+"%"
            var_val = match.group(2).strip()
            frags[var_name] = var_val
    #basic replacement
    for item in frags:
        data = data.replace(item, frags[item])
    #regex multi replacement
    for item in frags:
        base = item[1:-1]
        pat = r'%('+base+')\*(.*?)%'
        data = re.sub(pat, replacement, data)

# output to stdin to pandoc
print(data)




