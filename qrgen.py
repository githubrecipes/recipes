#!/usr/bin/python3

import qrcode
import sys

img = qrcode.make(sys.argv[1])

replacements = ["\"", ":", "<", ">", "|", "*", "?"]
title = sys.argv[2].lower().replace(" ", "-")
for item in replacements:
    title = title.replace(item, "")

file = title+".png"

img.save("./assets/"+file)

print("""
<div class=\"qrcode\">
    <img src=\"https://githubrecipes.com/assets/{}\" alt=\"{}\" width=\"300\" height=\"300\">
</div>
""".format(file, title))

