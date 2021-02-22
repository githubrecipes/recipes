import re
import sys

filename = sys.argv[1]
# filename = "./crockpot/shepardspie.md"
var_pat = r'(%.*?%)'
html_frags = [
#       replace this        with this
    ['%container%','<div class="container">' ],
    ['%sidebyside%','<div class="sidebyside">'],
    ['%enddiv%','</div>'],
    ['%noprint%','<div class="noprint">'],
]


with open(filename, 'r') as f:
    data = f.read()
    for item in html_frags:
        data = data.replace(item[0], item[1])

# output to stdin to pandoc
print(data)




