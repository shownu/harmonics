"""
first input filename with extension in doctitle
clear nos_to_skip
then uncomment print(j, k) and hit F5 to run
if code stops running with KeyError: 'OCTAVE_A', add the next number into nos_to_skip and rerun. repeat if necessary
then uncomment print(range(len(resp_dict))) and run. second number should be 1+ the above
now comment previously uncommented lines 
and uncomment lines which don't start with print
and run to output to excel
insert row at the top of excel file with appropriate titles
finally convert to table and save as .xlsm
"""

import json
import csv

doctitle = 'XXXXXXXXXXXXXXX.json'

nos_to_skip = {}

with open(doctitle, newline='') as f:
    resp_dict = json.load(f)

#    print(range(len(resp_dict)))
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for j in range(len(resp_dict)):
            if (not j in nos_to_skip):                    
                for k in range(len(resp_dict[j]['nb']['OCTAVE_A'])):
                    beam = str(k)
#                    print(j, k)
                    for i in range(len(resp_dict[j]['nb']['OCTAVE_A'][beam])):
#                        print(resp_dict[j]['nb']['OCTAVE_A'][beam])
#                        print(range(len(resp_dict[j]['nb']['OCTAVE_A'])))
                        row = (j, resp_dict[j]['clockTime'], k, i, resp_dict[j]['nb']['OCTAVE_A'][beam][i]['frequency'], resp_dict[j]['nb']['OCTAVE_A'][beam][i]['level'])
#                        print(row)
                        writer.writerow(row)  
