import pandas as pd
import math
import numpy as np
import sys

print(sys.argv)
if (len(sys.argv) != 2):
    print("describe.py <csv file>")
    exit()
    
try:
    dataset = pd.read_csv(sys.argv[1])
except:
    print(" No such file or directory: '" + sys.argv[1] +"'")
    exit()

def mean(l: list):
    if len(l) == 0:
        return float('NaN')
    return sum(l) / len(l)

def min(l: list):
    if len(l) == 0:
        return float('NaN')
    t = l[0]
    for i in l:
        if i < t:
            t = i
    return t

def max(l: list):
    if len(l) == 0:
        return float('NaN')
    t = l[0]
    for i in l:
        if i > t:
            t = i
    return t

def quartile(liste: list, k):
    if (len(liste) == 0):
        return float('NaN')
    liste.sort()
    n = len(liste)
    index = (n - 1) * k / 100
    if n < 1:
        return 0
    if index.is_integer():
        return liste[int(index)]
    else:
        bas = int(index)
        haut = bas + 1
        fraction = index - bas
        return liste[bas] + (liste[haut] - liste[bas]) * fraction

def std(l: list):
    if len(l) == 0:
        return float('NaN')
    moyenne = sum(l) / len(l)
    ecarts_carres = [(x - moyenne) ** 2 for x in l]
    variance = sum(ecarts_carres) / (len(l) - 1)
    return math.sqrt(variance)

def print_table(table):
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))

formated_list = [
    [""],
    ["count"],
    ["mean"],
    ["std"],
    ["min"],
    ["25%"],
    ["50%"],
    ["75%"],
    ["max"],
                 ]

for col in dataset.columns:
    l = dataset[col].values.tolist()
    if all(isinstance(x, (int, float)) for x in l) == False:
        continue

    filtred = [x for x in l if not math.isnan(x)]
    formated_list[0].append(col)
    formated_list[1].append(format(len(filtred), '.6f'))
    formated_list[2].append(format(mean(filtred), '.6f'))
    formated_list[3].append(format(std(filtred), '.6f'))
    formated_list[4].append(format(min(filtred), '.6f'))
    formated_list[5].append(format(quartile(filtred, 25), '.6f'))
    formated_list[6].append(format(quartile(filtred, 50), '.6f'))
    formated_list[7].append(format(quartile(filtred, 75), '.6f'))
    formated_list[8].append(format(max(filtred), '.6f'))



trunc_table = np.array(formated_list)

if len(formated_list[0]) > 9:
    indices_colonnes_a_supprimer = np.arange(6, trunc_table.shape[1]-5)
    trunc_table = np.delete(formated_list, indices_colonnes_a_supprimer, axis=1)
    trunc_table = np.insert(trunc_table, 6, '...', axis=1)

print_table(trunc_table)

