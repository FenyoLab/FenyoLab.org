
#===============================================================================
# Given a Microarray Dataset (samples in rows, genes in columns, class label in 1st column):
#    -> Perform a two-sample t-test to check for differential gene expression
#    -> For the 20 most differentially expressed genes (according to p-value of the t-test):
#         -> plot a histogram of their expression values
#         -> overlay the histogram with a Gaussian distribution
# Possible extensions:
#    -> add preprocessing before doing the test
#    -> add other statistical tests and give the user a choice of which test to perform 
#    -> Build a discriminative model from the top selected genes to predict group label
#===============================================================================


import pandas as pd
from scipy import stats
from numpy import mean, std
import matplotlib.pyplot as plt
from numpy import arange, ceil

from pandas import Series
    
def perform_tTest_one(exprValues, groupLabels):
    ## returns only p-value for each column
    groups = groupLabels.unique()
    sample1 = exprValues[groupLabels==groups[0]]
    sample2 = exprValues[groupLabels==groups[1]]
#     print "Sample: ", x.tolist()
#     print "Sample1: ", sample1
#     print "Sample2: ", sample2
    twoSampleTTest_results = stats.ttest_ind(sample1, sample2)
    return twoSampleTTest_results[-1]   ## p-value... Check the help file...

def perform_tTest_two(exprValues, groupLabels):
    ## returns t-statistic and p-value for each column 
    groups = groupLabels.unique()
    sample1 = exprValues[groupLabels==groups[0]]
    sample2 = exprValues[groupLabels==groups[1]]
    twoSampleTTest_results = stats.ttest_ind(sample1, sample2)
    return Series(twoSampleTTest_results, index=['t-statistic', 'p-value'])

def fill_subplot(subplot, x, groupLabels):
    groups = groupLabels.unique()
    sample1 = x[groupLabels==groups[0]].tolist()
    sample2 = x[groupLabels==groups[1]].tolist()
    ## Histograms
    subplot.hist(sample1, normed=True, edgecolor='r', fill=False, label=groups[0])
    subplot.hist(sample2, normed=True, edgecolor='b', fill=False, label=groups[1])

    ## Add Gaussian Curve
    xlim = subplot.get_xlim()
    xpoints = arange(xlim[0], xlim[1], step=0.01)
    
    mean1 = mean(sample1)
    std1 = std(sample1)
    density1 = stats.distributions.norm.pdf(xpoints, loc=mean1, scale=std1)
    subplot.plot(xpoints, density1, color='r')

    mean2 = mean(sample2)
    std2 = std(sample2)
    density2 = stats.distributions.norm.pdf(xpoints, loc=mean2, scale=std2)
    subplot.plot(xpoints, density2, color='b')
    
print

import ipdb
ipdb.set_trace()
dataMatrix = pd.read_table("/Users/hgrover/Downloads/leukemia.tab")

#==========================================================
# Basic exploration
#     1. no. of dimensions, shape etc.
#     2. columnNames, rowNames
#     3. number of members of each class
#==========================================================
# dataMatrix.<hit tab>
# type(dataMatrix)
# dataMatrix.ndim
# dataMatrix.shape
# dataMatrix.columns
# dataMatrix.index

##individual columns
# data.<Some Col>.tolist()
# data.<Some Col>.describe()
# data.Class.describe()
# data.Class.unique()
# data.Class.value_counts()

groupLabels = dataMatrix.Class
exprDF = dataMatrix.drop(labels=['Class'], axis=1) 

## Compare dataMatrix.shape vs. exprDF.shape


## Perform independent 2-sample t-test and sort values according to p-values
## Method 1: Write your own for loop; manage the return values yourself
for column in exprDF.columns:
    perform_tTest_one(exprDF[column], groupLabels)

## Check the documentation: exprDF.apply?    --> axis=0 => apply the function to each column
## Method 2: Use <DataFrame>.apply method to apply to each column of your expression matrix           

## 2a: Return only p-values
#tTest_pValues = exprDF.apply(perform_tTest_one, \
#                             axis=0, args=(groupLabels,))
#tTest_pValues_sortedAsc = tTest_pValues.order()
## Check top 5: tTest_pValues_sortedAsc[:5]

## 2b: Return both t-statistic and p-value
#tTest_results = exprDF.apply(perform_tTest_two, \
#                             axis=0, args=(groupLabels,))
#tTest_results_transpose = tTest_results.transpose()
#tTest_results_sortedAscByPVal = tTest_results_transpose.sort_index(by='p-value')
## Check top 5: tTest_results_sortedAscByPVal.ix[:5, :]

## Take top-20 differentially expressed features and plot their expression histograms with overlaid smooth distribution

## Make plots and save (Create a new function for this loop)
#noOfTopFeatures = 20
#noOfRows = 2
#noOfCols = 2
#noOfFigures = int(ceil(noOfTopFeatures/float(noOfRows*noOfCols)))
#for figIndex in xrange(noOfFigures):
#    share_x = None
#    share_y = None
#    fig = plt.figure(figIndex+1)
#    for plotIndex in range(0, noOfRows*noOfCols):
#        subplot = fig.add_subplot(noOfRows, noOfCols, \
#                                  plotIndex+1, \
#                                  sharex=share_x, sharey=share_y, \
#                                  title=tTest_pValues_sortedAsc.index[figIndex*noOfCols*noOfRows + plotIndex])
#        fill_subplot(subplot, \
#                     exprDF[tTest_pValues_sortedAsc.\
#                            index[figIndex*noOfCols*noOfRows \
#                                  + plotIndex]], \
#                     groupLabels)
#        share_x = subplot
#        share_y = subplot
#    fig.get_axes()[0].legend()
#    plt.savefig("/Users/hgrover/Desktop/plots/fig%d.pdf"%(figIndex+1), \
#                format='pdf')
#    for subplt in fig.get_axes():
#        fig.delaxes(subplt)
