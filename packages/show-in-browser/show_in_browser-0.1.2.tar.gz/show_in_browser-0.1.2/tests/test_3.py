# tests of plotly-to-browser function(s)
from show_in_browser import show_px_plot
import pandas as pd
import numpy as np
import plotly.express as px

def test_px_plot():
    df = pd.DataFrame({'score_1': np.random.normal(100, 10, 20),
                        'score_2': np.random.normal(100, 10, 20)})

    fig = px.scatter(df, x='score_1', y='score_2')

    show_px_plot(fig)

def test_px_plot_3D():
    # create dataframe
    df = pd.DataFrame({'score_1': np.random.normal(100, 10, 100),
                    'score_2': np.random.normal(1000, 2, 100),
                    'score_3': np.random.normal(10, 2, 100)})
    # create 3D scatterplot to show in browser
    fig = px.scatter_3d(df, x='score_1', y='score_2', z='score_3')

    show_px_plot(fig)

if __name__ == "__main__":
    test_px_plot()
    test_px_plot_3D()