#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
import matplotlib.pyplot as plt
 
labels = ['00', '01', '10', '11']
sizes = [40000, 404800, 180655, 598219]
colors = ['lightblue', 'steelblue', 'royalblue', 'mediumblue']
explode = (0.2, 0, 0, 0)

plt.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

plt.legend(labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()
'''
# txt -> csv

import csv

txt_file = r"feature1.txt"
csv_file = r"feature1_.csv"

# use 'with' if the program isn't going to immediately terminate
# so you don't leave files open
# the 'b' is necessary on Windows
# it prevents \x1a, Ctrl-z, from ending the stream prematurely
# and also stops Python converting to / from different line terminators
# On other platforms, it has no effect
in_txt = csv.reader(open(txt_file, "rb"), delimiter = '\t')
out_csv = csv.writer(open(csv_file, 'wb'))

out_csv.writerows(in_txt)