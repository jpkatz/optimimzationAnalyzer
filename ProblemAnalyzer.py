# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 17:06:25 2021

@author: Justin
"""
import pandas as pd
class problemAnalyzer():
    #converted
    CONVERTER = {0:'=',1:'>=',-1:'<='}
    CCOLUMNS = ['Constraint','RHS','Sense']
    COEF = 'Coef'
    OBJ = 'objective'
    OPT = 'OPTIMAL'
    EMPTY = 'No Name'
    
    def __init__(self, problem, autoBuild = False):
        self.name = problem.name
        if( autoBuild ):
            self.buildDataFrames(problem)
    
    def buildDataFrames(self, problem):
        constraints = list( problem.constraints.values())
        cData = []
        constraintNames = []
        variableInConstraint = []
        variableCoefInConstraint = []
        for constraint in constraints:
            name = constraint.name or self.EMPTY
            cData.append([name,
                          -constraint.constant,
                          self.CONVERTER[constraint.sense]
                          ])
            for cVar in constraint.keys():
                constraintNames.append(cVar.name)
                variableInConstraint.append(name)
                variableCoefInConstraint.append(constraint[cVar])
        objective = problem.objective
        for v in objective.keys():
            constraintNames.append(v.name)
            variableInConstraint.append(self.OBJ)
            variableCoefInConstraint.append(objective[v])
        multiIndex = pd.MultiIndex.from_arrays([constraintNames,
                                                variableInConstraint],
                                               names = ('Variable',
                                                        'Constraint')
                                               )
        varOptimal = []
        for var in problem.variables():
            varOptimal.append(var.varValue)
        self.variable_df = pd.DataFrame(variableCoefInConstraint, 
                                    index = multiIndex,
                                    columns = [self.COEF])
        self.optimal_df = pd.DataFrame(varOptimal,
                                       index = problem.variables(),
                                       columns = [self.OPT])
        self.constraint_df = pd.DataFrame(cData,
                                          columns = self.CCOLUMNS)


    def swap(self):
        self.variable_df = self.variable_df.swaplevel()
    def sort(self):
        self.variable_df = self.variable_df.sort_index()
    def swapNsort(self):
        self.variable_df = self.variable_df.swaplevel().sort_index()
