#!/usr/bin/python
import re
import sys
import json
import argparse
from pathlib import Path

import subprocess

def replacement(match):
    # re method
    return frags[per_wrap(match.group(1))]*int(match.group(2))

def per_wrap(item):
    return "%"+str(item)+"%"

def metadata_tags(data):
    #get metadata tags
    frags = {}
    metadata_pat = r'^(.*?):(.*?)$'
    for line in data.split("\n"):
        if line=="...":
            break
        match = re.match(metadata_pat, line)
        if match:
            var_name = per_wrap(match.group(1))
            var_val = match.group(2).strip()
            frags[var_name] = var_val
    return frags

def file_process(data, frags):
    #basic replacement
    for item in frags:
        data = data.replace(item, frags[item])
    #regex multi replacement
    for item in frags:
        base = item[1:-1]
        pat = r'%('+base+')\*(.*?)%'
        try:
            data = re.sub(pat, replacement, data)
        except:
            pass

    return data

def json_frags(json_data, frags, filename):
    # load in all of the frags
    generated_filename = filename.stem+".html"

    files = []
    for item in json_data:
        name = per_wrap(item)
        content = json_data[item]

        if type(content) is list:
            if content[0] == "file_content":
                with open(content[1], 'r') as fc:
                    frags[name] = fc.read()
                    files.append(name)
            elif content[0] == "input_file_name":
                frags[name] = filename.name
            elif content[0] == "output_file_name":
                frags[name] = generated_filename
            elif content[0] == "script":
                # content[1] path of script
                # content[2] names to pass to the script
                arguments = [content[1]]
                for item in content[2:]:
                    key = per_wrap(item)
                    if key in frags:
                        arguments.append(frags[key])
                    else:
                        arguments.append(item)
                out = subprocess.Popen(arguments, stdout=subprocess.PIPE)
                frags[name] = str(out.communicate()[0])[2:-3].replace("\\n", "\n")
        else:
            frags[name] = content

    for file in files:
        data = frags[file]
        for item in frags:
            data = data.replace(item, frags[item])
        frags[file] = data

    return frags








if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTML grep tool")

    parser.add_argument('-f', '--frags', dest="fragment_file", action="store", default="frags.json", help="Path to frag file for find and replace")
    parser.add_argument('input', action="store", help="Input file to match and replace")
    parser.add_argument("-o", "--output", dest="output", action="store", help="Output file to save results to. Default is stdout")

    args = parser.parse_args()

    filename = Path(args.input)

    with open(filename, 'r') as f:
        data  = f.read()
        frags = metadata_tags(data)

    with open(args.fragment_file, 'r') as f:
        json_data = json.loads(f.read())
        frags = json_frags(json_data, frags, filename)

    if "index" in filename.name:
        frags['%up%'] = 'https://githubrecipes.com'
    else:
        frags['%up%'] = 'index.html'

    output = file_process(data, frags)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        # output to stdin to pandoc
        print(output)



