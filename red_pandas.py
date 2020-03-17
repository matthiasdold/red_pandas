import pandas as pd
import pyperclip

from tabulate import tabulate
from source.plotting import pareto_plot, sankey_plot, box_whisker_plot
from source.save_transforms import sgroupby

# custom series object to keep slice and dice consistent
class RedPandasFrame(pd.DataFrame):
    '''
    RedPandas Data Frame main class as a wrapper around pandas.DataFrames enhancing basic functionality
    '''

    @property
    def _constructor(self):
        return RedPandasFrame

    @property
    def _constructor_sliced(self):
        return RedPandasSeries


    # implement public the methods
    def save_groupby(self, grp_dims, **kwargs):
        ''' A groupby replacing None with 'nan' to not accidentally drop groups with None '''
        return sgroupby(self, grp_dims, **kwargs)

    def pareto(self, variable, value, **kwargs):
        ''' Pareto plot of a given variable (x-axis) and value (y-axis) '''
        return pareto_plot(self, variable, value, **kwargs)

    def sankey(self, left, right, mass):
        return sankey_plot(self, left, right, mass)

    def boxplot(self, grp_dims, value_cols, **kwargs):
        ''' Boxplot of value_cols (one or multiple) provided a group dim (one or multiple) TODO: what is the aggregation (sum... but others possible)'''
        return box_whisker_plot(self, grp_dims, value_cols, **kwargs)

    def to_markdown(
        self, n = 10, **kwargs
    ) -> str:
        ''' Copy a markdown presentation of the first n rows to the clipboard buidling on tabulate'''
        pyperclip.copy(tabulate(self.loc[:n, :], headers='keys', tabletfmt='pipe', **kwargs))



class RedPandasSeries(pd.Series):
    @property
    def _constructor(self):
        return RedPandasSeries

    @property
    def _constructor_expanddim(self):
        return RedPandasSeries

    def to_markdown(
        self, n = 10, **kwargs
    ) -> str:
        '''
        Copy a markdown string representation of the series first n lines
        :param n: number of lines to consider
        :param kwargs: kwargs as used by tabulate
        :return: string in markdown representation on clipboard
        '''

        pyperclip.copy(tabulate(self.reset_index()[:n], headers=['index', self.name], tablefmt='pipe', **kwargs))


    #overwrite value counts to also return a RedPandasSeries object
    def value_counts(self, **kwargs):
        '''
        :param kwargs: kwargs as provided to pandas.value_counts
        :return: value count series, but as RedPandasSeries
        '''
        return RedPandasSeries(super(RedPandasSeries, self).value_counts(**kwargs))



