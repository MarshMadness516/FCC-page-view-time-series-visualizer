import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data, parse dates and set date column as index
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data, removing top and bottom 2.5% of values
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot with red line
    fig, ax = plt.subplots(figsize=(24, 8))
    ax.plot(df.index, df['value'], 'r')
    
    # Set axis labels and title of plot
    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy(deep=True)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    df_bar = df_bar.groupby(by=['year', 'month'], as_index=False).mean()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(9, 6.75))
    ax = df_bar.pivot(index='year', columns='month', values='value').plot.bar(ax=ax)
    # Change axis labels
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    # Change legend labels to month names
    handles, labels = plt.gca().get_legend_handles_labels()
    for i, l in enumerate(labels):
        labels[i] = pd.to_datetime(l, format='%m').month_name()
    plt.legend(handles, labels, title='Months')

    # Save image and return fig
    fig = ax.get_figure()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots with Seaborn
    fig, axs = plt.subplots(1,2, figsize=(20,6))
    # Draw year-wise plot on the first element in matplotlib axes array, changing color palette and flier style and size
    ax1 = sns.boxplot(data=df_box, x='year', y='value', hue='year', legend=False, palette='Set1', flierprops={'marker':'d', 'markersize': 2}, ax=axs[0])
    # Draw month-wise plot on the second element in matplotlib axes array, changing color palette and flier style and size, and ordering the data chronologically
    ax2 = sns.boxplot(
        data=df_box,
        x='month',
        y='value',
        hue='month',
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        legend=False,
        palette='husl',
        flierprops={'marker':'d', 'markersize':2},
        ax=axs[1]
        )
    # Set titles and axis labels for both plots
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')


    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
