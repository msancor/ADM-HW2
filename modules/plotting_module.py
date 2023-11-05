#Here we import the necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings

#Here we ignore the warnings that are shown when we use the seaborn library. Specifically we ignore the FutureWarning warnings.
warnings.simplefilter(action='ignore', category=FutureWarning)

#Here we set the style of the plots.
#First, we set as default that matplotlib plots text should be in LaTeX format.
plt.rcParams['text.usetex'] = True
#Here we set the font family to serif.
plt.rcParams['font.family'] = 'serif'
#Here we set the font size
plt.rcParams['font.size'] = 10
#Here we set the label size for axes
plt.rcParams['axes.labelsize'] = 10
#Here we set the label weight for axes
plt.rcParams['axes.labelweight'] = 'bold'
#Here we set the title size for axes
plt.rcParams['axes.titlesize'] = 10
#Here we set the ticks label size
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
#Here we set the legend font size
plt.rcParams['legend.fontsize'] = 10
#Here we set the figure title size
plt.rcParams['figure.titlesize'] = 15




def box_plot(data: pd.DataFrame, x: str = None, y: str = None, **kwargs) -> None:
    """
    Function that plots boxplots for the columns of a dataframe.

    Args:
        data (pd.DataFrame): Dataframe with the columns to plot.
        x (str, optional): Dataframe column to plot. Defaults to None.
        y (str, optional): Dataframe column to plot. Defaults to None.
        **kwargs: Keyword arguments to pass to the seaborn boxplot function.

    Returns:
        None
    """
    #Here we plot the boxplot using seaborn
    sns.boxplot(data=data, x=x, y=y, width=0.1, **kwargs)

def hist_plot(data: pd.DataFrame, x: str = None, y: str = None, **kwargs) -> None:
    """
    Function that plots the distribution of a dataframe column.

    Args:
        data (pd.DataFrame): Dataframe with the columns to plot.
        x (str, optional): Dataframe column to plot. Defaults to None.
        y (str, optional): Dataframe column to plot. Defaults to None.
        **kwargs: Keyword arguments to pass to the seaborn histplot function.

    Returns:
        None
    """
    #Here we plot the histogram using seaborn
    sns.histplot(data=data, x=x, y=y, **kwargs)

def bar_plot(data: pd.DataFrame, x: str = None, y: str = None, **kwargs) -> None:
    """
    Function that plots the distribution of a dataframe column.

    Args:
        data (pd.DataFrame): Dataframe with the columns to plot.
        x (str, optional): Dataframe column to plot. Defaults to None.
        y (str, optional): Dataframe column to plot. Defaults to None.
        **kwargs: Keyword arguments to pass to the seaborn barplot function.

    Returns:
        None
    """
    #Here we plot the bar plot using seaborn
    sns.barplot(data=data, x=x, y=y, **kwargs)

def heat_map(data: pd.DataFrame, **kwargs) -> None:
    """
    Function that plots a heat map for a dataframe.

    Args:
        data (pd.DataFrame): Dataframe to plot.
        **kwargs: Keyword arguments to pass to the seaborn heatmap function.

    Returns:
        None
    """
    #Here we plot the heat map using seaborn
    sns.heatmap(data=data, **kwargs)

def pie_chart(counts_list: list, labels_list: list = None, **kwargs) -> None:
    """
    Function that plots a pie chart.

    Args:
        counts_list (list): List of counts.
        labels_list (list, optional): List of labels. Defaults to None.
        **kwargs: Keyword arguments to pass to the matplotlib pie function.

    Returns:
        None
    """
    #Here we define a list called explode with the coefficients for the explosion of the pie chart. This is a form of highlighting a specific slice of the pie chart.
    explode = [0.1 for i in range(len(counts_list))]

    #Here we plot the pie chart using matplotlib. We use the autopct parameter to show the percentage of each slice. The startangle parameter is used to rotate the pie chart.
    plt.pie(counts_list, explode = explode, autopct='%1.1f%%', startangle=90, **kwargs)
    
    #We use the legend function to add a legend to the pie chart. We use the labels_list parameter to add the labels to the legend.
    plt.legend(labels_list, loc="upper center", bbox_to_anchor=(0.5, 0.05), ncol=5, fancybox=True, shadow=True)

def scatter_plot(data: pd.DataFrame, x: str = None, y: str = None, **kwargs) -> None:
    """
    Function that plots a scatter plot.

    Args:
        data (pd.DataFrame): Dataframe with the columns to plot.
        x (str, optional): Dataframe column to plot. Defaults to None.
        y (str, optional): Dataframe column to plot. Defaults to None.
        **kwargs: Keyword arguments to pass to the seaborn scatterplot function.

    Returns:
        None
    """
    #Here we plot the scatter plot using seaborn
    sns.scatterplot(data=data, x=x, y=y, **kwargs)

def hist_plot(data: pd.DataFrame, x: str = None, y: str = None, **kwargs) -> None:
    """
    Function that plots a histogram.

    Args:
        data (pd.DataFrame): Dataframe with the columns to plot.
        x (str, optional): Dataframe column to plot. Defaults to None.
        y (str, optional): Dataframe column to plot. Defaults to None.
        **kwargs: Keyword arguments to pass to the seaborn histplot function.

    Returns:
        None
    """
    #Here we plot the histogram using seaborn
    sns.histplot(data=data, x=x, y=y, **kwargs)
