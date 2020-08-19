#!/usr/bin/python3

import json
import sys

f=sys.argv[1]
commit=sys.argv[2]
data=""

with open(f,'r') as j_file:
    data = json.load(j_file)

data[0]['commit'] = commit

with open(f,'w') as j_file:
    json.dump(data, j_file)
