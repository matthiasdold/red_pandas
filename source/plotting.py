# -----------------------------------------------
# some plotting routines commonly used on data frame data
# keeping it simple with only matplotlib for a start, plotly for sankey
# TODO: Implement html capabilities, ideally standalone plots like with express plotly...
# -----------------------------------------------



import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def pareto_plot(df, variable: str, value: str) -> plt.figure:
    '''

    :param df: red_pandas data frame
    :param variable: Column name of x-axis
    :param value: Column name of y-axis
    :return:
        pyplot.figure object
    '''

    dfg = df.save_groupby(variable)[value].sum().sort_values(ascending=False).reset_index()
    dfg['cum_perc_value'] = dfg[value].cumsum()/dfg[value].sum()

    fig, ax = plt.subplot()

    ax.bar(dfg[variable], dfg[value], color='b')
    #TODO --> check if matplotlib colors can be defined in a css

    ax2 = ax.twinx()
    ax2.plot(dfg[variable], dfg['cum_perc_value'], color='r')

    plt.setp(ax.get_xticklabels(), rotation=30, ha='right', rotationmode='anchor', size=6)
    plt.setp(ax2.get_xticklabels(), rotation=30, ha='right', rotationmode='anchor', size=6)

    plt.show()

    return fig

def sankey_plto(df, left: str, right: str, mass: float) -> plt.axis:
    '''

    :param df: red_pandas data frame
    :param left: column name for left values
    :param right: column name for right values
    :param mass: values for connection strenght from left to right
    :return:
        matplotlib axis object
    '''

    dfg = df.save_groupby([left, right])[mass].sum().sort_values(ascending=False).reset_index()
    dfg = dfg.sort_values(by=left).reset_index(drop=True)                                           # reset needed for correct counting

    cleft = dfg[left].astype('category')
    cright = dfg[right].astype('category')

    label = list(cleft.cat.categories) + list(cright.cat.categories)
    source = list(cleft.cat.categories)
    target = list(cright.cat.codes) + list(cleft.cat.codes.unique())

    value = list(dfg[mass])

    fig = go.Figure(
        data=[
            go.Sankey(
                node = dict(
                    pad = 15,
                    thickness = 20,
                    line = dict(
                        color = 'black',
                        width = 0.5
                    ),
                    label = label,
                    color = 'blue'
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value
                )
            )
        ]
    )

    fig.update_layout(font_size=32, hoverlabel={'font': {'size': 32}})
    fig.write_html('last_fig.html', auto_open=True)

    return fig


def box_whisker_plot(df, grp_dims: list, value_cols: list, violin=False) -> plt.figure:
    '''

    :param df: red_pandas data frame
    :param grp_dims: list of columns names to group by
    :param value_cols: list of value columns to aggregate on
    :param violin: bool for violin plot yes/no -> default is False == normal box whiskers
    :return:
        matplotlib.pyplot figure object
    '''


    dt = df.copy().loc[:, grp_dims + value_cols]

    #TODO --> validate this line
    dt['aux'] = df.save_groupby(grp_dims).cumcount() + 1                                    # running count per group

    dfg = dt.save_groupby(grp_dims + 'aux')[value_cols].sum().unstack(grp_dims)

    # if we have multiple indeces -> multiple value cols -> create multiple lines

    #TODO --> check else case
    if type(dfg.columns) == pd.MultiIndex:
        fig, axs = plt.subplots(len(dfg.columns.levels[0]), 1, sharex=True)

        for i, val in enumerate(dfg.columns.levels[0]):
            data = dfg.iloc[:, dfg.columns.get_level_values(0) == val]
            data.columns = data.columns.droplevel()

            if len(dfg.columns.levels[0]) == 1:
                ax = axs
            else:
                ax = axs[i]

            ax = _create_box_plot_axis(ax, data, violin)
            ax.set_title(val)

            # further settings
            ax.grid(False)

    return fig


def _create_box_plot_axis(ax: plt.Axes, data, violin: Optional[bool] = False) -> plt.Axes:
    '''

    :param ax: a matplotlib.pyplot.Axes to plot to
    :param data: red pandas data frame
    :param violin: bool for violin plot yes/no -> default is False == normal box whiskers
    :return:
        matplotlib.pyplot.Axes object
    '''

    labels = []
    if type(data.columns) == pd.MultiIndex:
        for i in range(len(data.columns)):
            label = ''
            for j in range(len(data.columns.levels)):
                label += str(data.columns.get_level_values(j)[i]) + '_'

            labels.append(label[0:-1])
    else:
        labels = list(data.columns)


    if violin:
        ax.violinplot(data, showmedians=True, showextrema=False)
    else:
        data.boxplot(ax=ax)

    ax.set_xticklabels(labels)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    return ax
