# -*- coding: utf-8 -*-

first_names = []
with open('names-raw.txt', 'r') as fin:
    for line in fin:
        name = line.split()[0]
        # Clean out wiki reference symbols
        name = name.replace("†", "")
        name = name.replace("'s", "")
        if name not in first_names:
            first_names.append(name)

with open('names-clean.txt', 'w') as fout:
    for name in first_names:
        fout.write('%s\n' % name)
