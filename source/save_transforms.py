# This file contains transformations for pandas data frames which are considered "save" in my understanding
# "Save" is to be understood as not dropping any  'nan' values while grouping etc.
import numpy as np


def sgroupby(df, grp_dims, fill_nans=True, **kwargs):
    '''

    :param df: pandas data frame
    :param grp_dims: List of column names to groupby
    :param fill_nans: optional bool with default "True", whether to replace nan values with a 'nan' string or numeric nan
    :param kwargs: additional kwargs as used by pandas.DataFrame.groupby()
    :return:
        grouped data frame
    '''


    # also offer the possibility to just pass a string as grp_dims
    if type(grp_dims) == str:
        grp_dims = [grp_dims]


    # find nan values und group dims and report on them
    nan_cols = [c for c in df.columns if any(df[c].isna())]
    if nan_cols != []:
        for c in nan_cols:
            print("Found {} nan values in columns {}".format(sum(df[c].isna()), c))


    # replace nan values depending on data type
    if nan_cols != []:
        print("Continue with filling nans with 'nan' or 0 in a copy")
        replace_map = {}

        for c in nan_cols:
            replace_map[c] = df[c].isna()
            if df[c].dtype in ['int32', 'int64', 'float']:
                df[c].fillna(0)
            else:
                df[c].fillna('nan')

        dfg = df.groupby(grp_dims, **kwargs)
    else:
        dfg =  df.groupby(grp_dims, **kwargs)

    # replace to normal
    for c in replace_map.keys():
        df.loc[replace_map[c], c] = np.nan

    return dfg
