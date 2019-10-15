#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
5. Feature Normalization - [0,1]
'''
import pandas as pd
import numpy as np

# Read file - Dataframe
feat_Table = pd.read_csv('feature1.txt',delimiter='\t') 

# Create new Dataframe
feat_Normal = pd.DataFrame()

# Normalization - [0,1]
for i in list(feat_Table.columns):
	# First three header - no need to normalize
    if i in ['url', 'is_malicious']:
        feat_Normal[i]=feat_Table.ix[:,i]      # pandas.DataFrame.ix[row, column]
    else:
        line = feat_Table.ix[:,i]
        mean_ = line.mean()
        # std_ = line.std()
        # feat_Normal[i] = (line - mean_) / std_
        
        max_ = line.max() 
        min_ = line.min()
        feat_Normal[i] = (line - mean_) / (max_ - min_)

        # Decimal round to five
        feat_Normal[i] = feat_Normal[i].round(decimals=5)
    print 'Feature Normalization %s'%i

# Write the file
feat_Normal.to_csv('feature2.txt', sep='\t')
