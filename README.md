# optimimzationAnalyzer
Helps analyze pulp optimization problems

The idea is to make it easy to debug optimization problems using the PuLP library. If we think about variables being associated to constraints with coefficients, and constraints being associated to variabled, there is a natural representation using a pandas dataframe.

The example file is used to showcase how the dataframes can be used. In the file, a bin packing problem is considered. In this problem fruit is being packed into bins and some fruits are not allowed together.
