import pandas as pd



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




class RedPandasSeries(pd.Series):
    @property
    def _constructor(self):
        return RedPandasSeries

    @property
    def _constructor_expanddim(self):
        return RedPandasSeries

    def to_markdown(
        self, n: Optional[int] = 10, **kwargs
    ) -> Optional[str]:
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



