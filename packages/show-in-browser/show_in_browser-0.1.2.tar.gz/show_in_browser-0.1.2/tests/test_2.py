# tests of matplotlib-to-browser function(s)
from show_in_browser import show_plt_plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# some test data
df = pd.DataFrame({'score_1': np.random.normal(100, 10, 100),
                'score_2': np.random.normal(1000, 2, 100),
                'score_3': np.random.normal(10, 2, 100)})

# create another dataframe
df2 = pd.DataFrame({'score_1': np.random.normal(200, 10, 100),
                'score_2': np.random.normal(-1000, 2, 100),
                'score_3': np.random.normal(-10, 2, 100)})

def test_plt_plot():
    # create 2D scatterplot to show in browser
    plt.figure()
    plt.scatter(df['score_1'], df['score_2'])
    show_plt_plot()

def test_plt_plot_from_fig_objects():    
    # create first 2D scatterplot to show in browser
    fig1 = plt.figure()
    plt.scatter(df['score_1'], df['score_2'])

    # create first 2D scatterplot to show in browser
    fig2 = plt.figure()
    plt.scatter(df2['score_1'], df2['score_2'])

    # show plots (deliberately in reverse order)
    show_plt_plot(fig2)
    show_plt_plot(fig1)

def test_plt_plot_3D():
    # create 3D scatterplot to show in browser
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['score_1'], df['score_2'], df['score_3'])
    show_plt_plot()

def test_plt_plot_3D_interact():
    # create 3D scatterplot to interact with in browser
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['score_1'], df['score_2'], df['score_3'])
    show_plt_plot(interact=True)

def test_plt_plot_3D_interact_multiple_plots():    
    # create first 3D scatterplot to interact with in browser
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['score_1'], df['score_2'], df['score_3'])

    # create second 3D scatterplot to interact with in browser
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.scatter(df2['score_1'], df2['score_2'], df2['score_3'])
    show_plt_plot(interact=True)

def test_plt_plot_3D_interact_multiple_plots_2():
    # create first 3D scatterplot to interact with in browser
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['score_1'], df['score_2'], df['score_3'])

    # create second 3D scatterplot to interact with in browser
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.scatter(df2['score_1'], df2['score_2'], df2['score_3'])

    # create first 2D scatterplot to show in browser
    fig3 = plt.figure()
    plt.scatter(df2['score_1'], df2['score_2'])
    show_plt_plot(interact=True)

if __name__ == "__main__":
    test_plt_plot()
    test_plt_plot_from_fig_objects()
    test_plt_plot_3D()  
    test_plt_plot_3D_interact()
    test_plt_plot_3D_interact_multiple_plots()
    test_plt_plot_3D_interact_multiple_plots_2()