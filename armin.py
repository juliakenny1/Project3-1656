import csv
import sys
import os
import re
import sys
from itertools import combinations

class Armin():

    def apriori(self, input_filename, output_filename, min_support_percentage, min_confidence):
        """
        Implement the Apriori algorithm, and write the result to an output file

        PARAMS
        ------
        input_filename: String, the name of the input file
        output_filename: String, the name of the output file
        min_support_percentage: float, minimum support percentage for an sets
        min_confidence: float, minimum confidence for an association rule to be significant

        """
        numBas = []
        sets = set(())
        if os.path.isfile(os.path.join(os.getcwd(), input_filename)): #looking at file
            with open(input_filename, 'r') as file:
                read = csv.reader(file, delimiter='\n', quotechar='|')
                for row in read:
                    r = ','.join(row).split(',')[1:]
                    r = {i.strip() for i in r}
                    k = [i.strip() for i in r]
                    sets = sets.union(r)
                    numBas.append(r)
            sets = list(sets)
            sets.sort()

        v = []
        support_index = []
        #num items
        for i in range(len(sets) + 1):
            combos = combinations(sets, i + 1) #subset combos
            for i in combos: #iterations
                i = set(i)
                count = 0
                for k in numBas:
                    k = set(k)
                    if i.issubset(k):
                       count += 1
                sup = count / len(numBas)
                if sup >= min_support_percentage:
                    i = list(i)
                    i.sort()
                    v.append(i)
                    support_index.append(sup)
                elif len(i) == 1:
                    i = list(i)
                    sets.remove(i[0])

        with open(output_filename, "w", newline="") as f:
            for i in range(len(v)):
                row = csv.writer(f)
                c = v[i]
                c.insert(0, 'S')
                c.insert(1, '%.4f' % support_index[i])
                row.writerow(c)
            sub = v.copy()
            sub = [i[2:] for i in sub]
            us = v.copy()
            us = {(str(i[2:])): i[1] for i in us}

            for x in combinations(sub, 2):
                x = list(x)
                y = set(x[0])
                l = set(x[1])
                un = y.union(l)
                un = list(un)
                un.sort()

                if str(un) in us:
                    usp = float(us[str(un)])
                    first = list(y)
                    first.sort()
                    second = list(l)
                    second.sort()

                    if len(y.intersection(l)) == 0:
                        row = csv.writer(f, quoting=csv.QUOTE_NONE, quotechar=None, escapechar='\\')
                        fsp = float(us[str(first)])
                        ssp = float(us[str(second)])
                        c2 = usp / ssp
                        c1 = usp / fsp


                        if c1 >= min_confidence:
                            row.writerow(['R'] + [str('%.4f' % usp)] +
                                        [str('%.4f' % c1)] + first + ['\'=>\''] + second)

                        if c2 >= min_confidence:
                            row.writerow(['R'] + [str('%.4f' % usp)] +
                                        [str('%.4f' % c2)] + second + ['\'=>\''] + first)



if __name__ == "__main__":
    armin = Armin()
    armin.apriori('input.csv', 'output.sup=0.5,conf=0.7.csv', 0.5, 0.7)
    armin.apriori('input.csv', 'output.sup=0.5,conf=0.8.csv', 0.5, 0.8)
    armin.apriori('input.csv', 'output.sup=0.6,conf=0.8.csv', 0.6, 0.8)
