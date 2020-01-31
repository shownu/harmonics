import json
import csv

nos_to_skip = {45, 48, 56, 59, 70, 373, 383, 393, 403, 413, 424, 434, 578, 582, 610, 611, 660, 663, 674, 822, 857, 973, 984}

with open('minch-1-Nov-2019.json', newline='') as f:
    resp_dict = json.load(f)

    print(range(len(resp_dict)))
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for j in range(len(resp_dict)):
            if (not j in nos_to_skip): 
                    row = (j, resp_dict[j]['clockTime'], resp_dict[j]['bb']['OCTAVE_D'])
                    # print(row)
                    writer.writerow(row)
