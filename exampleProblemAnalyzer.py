# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:25:34 2021

@author: Justin
"""

import ProblemAnalyzer as pa
from pulp import *

def getAllVariableNames(fruits,binIds):
    return [assignmentLabel(fruit,binId) 
            for fruit in fruits for binId in binIds]

def assignmentLabel(fruit,binId):
    return fruit + '_' +str(binId)

#simple bin packing
fruits = ['Orange','Pineapple','Watermelon']
weights = [5,10,20]
items = dict(zip(fruits,weights))
notAllowed = {'Orange':'Pineapple', 'Pineapple':'Orange'}
maxCapBin = 20
binIds = ['Bin' + str(i) for i in range(len(items)+1)] #every item gets a bin,one extra

problem = LpProblem('Bin Packing with Fruit', LpMinimize)

assignmentVars = LpVariable.dicts('Assign',
                           getAllVariableNames(fruits,binIds),
                           cat = LpBinary
                           )
binUsedVars = LpVariable.dicts('Is used',
                               [binId for binId in binIds],
                               cat = LpBinary)

problem += lpSum([binUsedVars[i] for i in binUsedVars]),'objective'

#constraint, can only assign to one bin
for fruit in fruits:
    problem += lpSum([assignmentVars[assignmentLabel(fruit,binId)]
                      for binId in binIds]) == 1, 'Single Assignment:' + fruit

#constraint, bin is used
for binId in binIds:
    problem += lpSum([assignmentVars[assignmentLabel(fruit,binId)]
                      for fruit in fruits] - binUsedVars[binId]) <= 0, 'BinUsed:'+binId

#constraint, respect capacity
for binId in binIds:
    problem += lpSum([items[fruit] * assignmentVars[assignmentLabel(fruit,binId)]
                      for fruit in fruits]) <= maxCapBin,'Capacity:'+binId

#constraint, conflict
for binId in binIds:
    for fruit in fruits:
        try:
            fruit1 = fruit
            fruit2 = notAllowed[fruit]
            problem += lpSum(assignmentVars[assignmentLabel(fruit1,binId)]
                             +assignmentVars[assignmentLabel(fruit2,binId)]) <=1,'Conflict:'+fruit1+fruit2+binId
        except:
            pass
solution_found = problem.solve()

#creating problem analyzer
problem_df = pa.problemAnalyzer(problem,True)
print('---Raw results---')
#raw prints
print(problem_df.variable_df)
print('---')
print(problem_df.constraint_df)
print('---')
print(problem_df.optimal_df)

#some nice things
print('---sorting---')
problem_df.sort()
print(problem_df.variable_df)
print('---swap to constraint focus---')
problem_df.swap()
problem_df.sort()
print(problem_df.variable_df)