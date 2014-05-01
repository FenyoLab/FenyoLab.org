
#===============================================================================
# Given a Microarray Dataset (samples in rows, genes in columns, class label in 1st column):
#    -> Perform a simple group-wise normalization on each gene {x_norm = (x-mu)/sigma}
#    -> Perform a two-sample t-test to check for differential gene expression
#    -> For the 10 most differentially expressed genes (according to p-value of the t-test):
#         -> plot a histogram of their expression values
#         -> overlay the histogram with a Gaussian distribution
# Possible extensions:
#    -> add other kinds of preprocessing steps and give the user choices
#    -> add other statistical tests and give choices to the user 
#    -> Build a machine-learning model from the top selected genes
#===============================================================================


import pandas as pd
from numpy import mean, std, arange
from scipy import stats
from math import ceil
import matplotlib.pyplot as plt


def standardize(exprValues):
    return (exprValues - mean(exprValues))/std(exprValues, ddof=1)
    
def perform_tTest(exprValues, groupLabels):
    groups = groupLabels.unique()
    sample1 = exprValues[groupLabels==groups[0]].tolist()
    sample2 = exprValues[groupLabels==groups[1]].tolist()
#     print "Sample: ", x.tolist()
#     print "Sample1: ", sample1
#     print "Sample2: ", sample2
    twoSampleTTest_results = stats.ttest_ind(sample1, sample2)
    return twoSampleTTest_results[-1]   ## p-value... Check the help file...

def fill_subplot(subplot, x, groupLabels):
    groups = groupLabels.unique()
    sample1 = x[groupLabels==groups[0]].tolist()
    sample2 = x[groupLabels==groups[1]].tolist()
    
    ## Histograms
    subplot.hist(sample1, normed=True, edgecolor='r', fill=False, label=groups[0])
    subplot.hist(sample2, normed=True, edgecolor='b', fill=False, label=groups[1])

    ## Get X-axis limits
    xlim = subplot.get_xlim()
    xpoints = arange(xlim[0], xlim[1], step=0.01)
    
    ## Add Gaussian Curves
    mean1 = mean(sample1)
    std1 = std(sample1, ddof=1)
    density1 = stats.distributions.norm.pdf(xpoints, loc=mean1, scale=std1)
    subplot.plot(xpoints, density1, color='r')

    mean2 = mean(sample2)
    std2 = std(sample2, ddof=1)
    density2 = stats.distributions.norm.pdf(xpoints, loc=mean2, scale=std2)
    subplot.plot(xpoints, density2, color='b')
    
print

# import ipdb
# ipdb.set_trace()
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

## Now show that the index in Series object and that in the exprDF object can be used together to align them together...  
## This will be used in standardization step, where we want to separate out each group

## Standardize columns/features
## Can't step into this function... so run it for one particular column and show that exprDF_colStd gives the correct results
## standardize(exprDF[0], classLabels)
## Check the documentation: exprDF.apply?    --> axis=0 => apply the function to each column
exprDF_colStd = exprDF.apply(standardize, axis=0)

## Perform 2-sample t-test and sort values according to p-values
## Note that the Series object returned has, as index, 
## the column names of the expression matrix...

tTest_pValues = exprDF_colStd.apply(perform_tTest, \
                                    axis=0, args=(groupLabels,))
# tTest_pValues = exprDF.apply(perform_tTest, \
#                                     axis=0, args=(groupLabels,))
tTest_pValues_sortedAsc = tTest_pValues.order()


## Take top-20 differentially expressed features and plot their 
## standardized expressions. Save the plots.
noOfTopFeatures = 20
noOfRows = 2
noOfCols = 2
noOfFigures = int(ceil(noOfTopFeatures/float(noOfRows*noOfCols)))
for figIndex in xrange(noOfFigures):
    fig = plt.figure(figIndex+1)
    for plotIndex in range(0, noOfRows*noOfCols):
        subplot = fig.add_subplot(noOfRows, noOfCols, plotIndex+1, \
                                  title=tTest_pValues_sortedAsc.index[figIndex*noOfCols*noOfRows + plotIndex])
        fill_subplot(subplot, \
                     exprDF_colStd[tTest_pValues_sortedAsc.index[figIndex*noOfCols*noOfRows \
                                                                 + plotIndex]], \
                     groupLabels)
    fig.get_axes()[0].legend()
    plt.savefig("/Users/hgrover/Desktop/plots/fig%d.pdf"%(figIndex+1), format='pdf')
    

## HW-4: Make pairwise scatter plots for top-n (n=4) genes, one pair (plot) per figure
##       Check documentation (plt.scatter?) or web, for scatter plots
##            -> Color for scatterplot should be different for the two different groups (Ex. blue for AML, red for ALL)
#             ## Add labels to the scatter plot, so that you can add a legend to the plotlater
##       Make one plot interactively, just like we discussed in class for histograms
##       Then use code in this script to do it in batch mode... 
# n = 4
# for x in xrange(n-1):
#     for y in xrange(x+1, n):
#         ## Extract expression values for gene number 'x' and gene number 'y'
#         ## Create a Figure
#         ## Add a subplot... fig.add_subplot(1,1,1)
#         ## Write a function to fill the subplot with scatter plot 
#         fill_subplot_scatter(subplot, expr_gene_x, expr_gene_y, groupLabels)
#         ## save the figure