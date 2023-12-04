# tests of dataframe, matplotlib and plotly-to-browser function(s)
from show_in_browser import show_df, show_plt_plot, show_px_plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# some test data
df = pd.DataFrame({'score_1': np.random.normal(100, 10, 100),
                'score_2': np.random.normal(1000, 2, 100),
                'score_3': np.random.normal(10, 2, 100)})

# create another dataframe
df2 = pd.DataFrame({'score_1': np.random.normal(200, 10, 100),
                'score_2': np.random.normal(-1000, 2, 100),
                'score_3': np.random.normal(-10, 2, 100)})

def test_df_plt_px_plots():
    # create first 2D scatterplot to show in browser
    fig1 = plt.figure()
    plt.scatter(df['score_1'], df['score_2'])
    show_plt_plot()

    # show a dataframe
    show_df(df)

    # create first 2D scatterplot to show in browser
    fig2 = plt.figure()
    plt.scatter(df2['score_1'], df2['score_2'])
    show_plt_plot()

    # show another dataframe
    show_df(df2)

    # create 3D scatterplot to show in browser
    fig3 = px.scatter_3d(df, x='score_1', y='score_2', z='score_3')
    show_px_plot(fig3)

def test_df_plt_px_plots_from_fig_objects():

    # show a dataframe
    show_df(df2)

    # create first 2D scatterplot to show in browser
    fig1 = plt.figure()
    plt.scatter(df['score_1'], df['score_2'])

    # create first 2D scatterplot to show in browser
    fig2 = plt.figure()
    plt.scatter(df2['score_1'], df2['score_2'])

    # show another dataframe
    show_df(df)

    # create 3D scatterplot to show in browser
    fig3 = px.scatter_3d(df, x='score_1', y='score_2', z='score_3')

    # show plots (deliberately out of order)
    show_plt_plot(fig2)
    show_px_plot(fig3)
    show_plt_plot(fig1)

if __name__ == "__main__":
    test_df_plt_px_plots()
    test_df_plt_px_plots_from_fig_objects()