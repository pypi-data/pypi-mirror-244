import pandas as _pd
import webbrowser as _webbrowser
import os as _os
from time import sleep
import matplotlib as _mpl
import matplotlib.pyplot as _plt
import aspose.words as _aw
import warnings as _warnings
class MPLBackendWarning(UserWarning):
    pass

def show_df(df, name='temp', decimal_places=3, delete=True, delete_pause=1):
    """Show a pandas dataframe in the default browser, from the command line.

    Parameters
    ----------
    df : pandas DataFrame (can also be a Series)
        The DataFrame (or Series) to be displayed in the browser.

    name : str
        The name of the temporary HTML file generated (which contains the 
        information from the dataframe). This is useful for keeping track of 
        what the dataframe shows if you are opening multiple tabs showing
        different dataframes. In most browsers the name of the temporary file
        will be displayed on the tab that displays that particular dataframe.
        You may want to use names like "control_group" etc. to make it clearer
        what information is shown on the dataframe in that tab. Note: the name
        supplied does NOT need a file extension.

    decimal_places: int
        Temporarily set what how many decimal places to show numbers to. Default
        is 3.

    delete : Bool
        Boolean indicating whether to delete the temporary HTML file after
        it is shown in the browser. Default is True.    

    delete_pause : Bool
        Number indicate how long to wait before deleting the temporary HTML file.
        You may want to change this if your browser is taking a long time
        to open the file (e.g. so it is getting deleted before it is shown).
        Default is 1 second. 

    Example
    ----------

    from show_in_browser import show_df
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # create dataframe
    df = pd.DataFrame({'score_1': np.random.normal(100, 10, 100),
                    'score_2': np.random.normal(1000, 2, 100),
                    'name': np.repeat(['A', 'B'], 50)})

    # show the dataframe in browser
    show_df(df)
    """
    # coerce input to dataframe (user may often want to use it on a
    # pandas series e.g. the output of groupby etc.)
    df = _pd.DataFrame(df)

    # use a specific number of decimal places for display, without altering 
    # data
    with _pd.option_context('display.precision', decimal_places):

        # convert the dataframe to HTML
        html_df = df.to_html()

        # write a temporary HTML file
        with open(name+'.html', 'w') as file:
            file.write(html_df)

        # display the dataframe in browswer
        _webbrowser.get().open('file://' + _os.path.realpath(name+'.html'))

        # delete the temporary file (after a pause to allow display in browser)
        if delete == True:
            sleep(delete_pause)
            _os.remove(_os.path.realpath(name+'.html'))


def show_plt_plot(fig=None, name="temp_plot", delete=True, delete_pause=1,
                  interact=False):
    """Show a matplotlib.pyplot plot in the default browser, from the command
     line.

     Works like plt.show() - run it after your plotting commands. Or, if you 
     have saved your plot as a variable (e.g. called `my_plot`) then you can
     pass it to this function using the argument `show_plt_plot(fig=my_plot)`.

    Parameters
    ----------

    fig: matplotlib.figure.Figure
        The matplotlib graph object which you want to open in a browser. 
        If no figure is supplied, then the current figure will be shown.
        Default is None.

    name : str
        The name of the temporary HTML file generated (which contains the 
        plot). Note: the name supplied does NOT need a file extension.

    delete : Bool
        Boolean indicating whether to delete the temporary HTML file after
        it is shown in the browser. Default is True.    
        
    delete_pause : Bool
        Number indicate how long to wait before deleting the temporary HTML file.
        You may want to change this if your browser is taking a long time
        to open the file (e.g. so it is getting deleted before it is shown).
        Default is 1 second. 
    
    interact : Bool
        Set whether to display your matplotlib plot(s) interactively (e.g. so
        you can rotate a 3D scatterplot). NOTE: we **strongly** recommend using
        plotly if you want interactive plots - you will have to change the
        matplotlib backend to 'WebAgg' if you want to use matplotlib. If using
        matplotlib interactively, you should only run `show_plt_plot()` once
        and all your plots will be shown in the same tab (e.g. you do not have
        to run it for each separate plot). Default is False. 

    Example
    ----------
    from show_in_browser import show_plt_plot
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # create dataframe
    df = pd.DataFrame({'score_1': np.random.normal(100, 10, 100),
                       'score_2': np.random.normal(1000, 2, 100),
                       'score_3': np.random.normal(10, 2, 100)})

    # create 3D scatterplot to show in browser
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df['score_1'], df['score_2'], df['score_3'])

    # show in browser
    show_plt_plot()  
    """
    # if the `interact` argument is set to True...
    if interact == True:

        # check that no figure object has been supplied (WebAgg backend
        # does not support passing a figure object e.g. plt.show() will only 
        # work with the currently open figure)
        assert fig == None, """
If using matplotlib interactively in a browser, you cannot supply 
`show_plt_plot()` with a figure object. Only the currently open figure will be 
displayed. Please remove the `fig` argument and try again.
"""
        # get a record of the current matplotlib backend
        original_mpl_backend = _plt.get_backend()

        # show the plot, if the appropriate matplotlib backend is already
        # selected
        if original_mpl_backend == 'WebAgg':
            # show the plot
            _plt.show()

        # else instruct the user how to proceed
        else:
            _warnings.warn(f"""
Matplotlib backend must be set to "WebAgg" in order to display in browser for
interactive use. Before you run `show_plt_plot(interact=True)`, 
please run the following commands first:
```
import matplotlib
matplotlib.use("WebAgg")
```
           
If you want to go back to your original backend settings, you can run the 
following commands to restore to your original settings: 
```
import matplotlib
matplotlib.use({original_mpl_backend})
```
""", MPLBackendWarning)

    # if the plot is NOT interactive...
    if interact == False:

        # set fig to be the current figure, if no fig argument is supplied
        if fig == None:
            fig = _plt.gcf()
        
        # store some filenames (png and html)
        name_png = name+".png"
        name_html = name+".html"

        # sometimes aspose-words creates a junk file like "temp_plot.001.png",
        # store its name as a string so it can be deleted
        junk_name = name+".001.png" 

        # save the current figure
        _plt.figure(fig)
        _plt.savefig(name_png)

        # create a temporary html file containing the figure
        doc = _aw.Document()
        _aw.DocumentBuilder(doc).insert_image(_os.path.realpath(name_png))
        doc.save(name_html)

        # open the temporary html file, then close the matplotlib figure (to
        # avoid errors)
        _webbrowser.get().open('file://' + _os.path.realpath(name_html))

        # delete the temporary file (after a pause to allow display in browser)
        if delete == True:
            sleep(delete_pause)
            _os.remove(_os.path.realpath(name_png))
            _os.remove(_os.path.realpath(name_html))
            if junk_name in _os.listdir():
                # if aspose-words created a junk file, delete it
                _os.remove(_os.path.realpath(junk_name)) 

def show_px_plot(fig, name="temp_plot", delete=True, delete_pause=1):
    """Show a plotly.express plot in the default browser, from the command line.

    Works like plt.show(fig). E.g. save your plot as a variable (like `my_plot`) 
    and then use `show_px_plot(fig=my_plot)`.

    Parameters
    ----------
    fig: plotly.graph_objs._figure.Figure
        The plotly graph object which you want to open in a browser.

    name : str
        The name of the temporary HTML file generated (which contains the 
        plot). Note: the name supplied does NOT need a file extension.

    delete : Bool
        Boolean indicating whether to delete the temporary HTML file after
        it is shown in the browser. Default is True.    
        
    delete_pause : Bool
        Number indicate how long to wait before deleting the temporary HTML file.
        You may want to change this if your browser is taking a long time
        to open the file (e.g. so it is getting deleted before it is shown).
        Default is 1 second. 

    Example
    ----------
    from show_in_browser import show_px_plot
    import pandas as pd
    import numpy as np
    import plotly.express as px
    # create a dataframe
    df = pd.DataFrame({'x': np.random.normal(100, 10, 20),
                        'y': np.random.normal(100, 10, 20)})
                        
    # create a plotly graph
    fig = px.scatter(df, x='x', y='y')

    # show the graph in browser
    show_px_plot(fig)  
    """
    # write a temporary html file and open it in the browser
    name_html = name+".html"
    fig.write_html(name_html)
    _webbrowser.get().open('file://' + _os.path.realpath(name_html))

    # delete the temporary file (after a pause to allow display in browser)
    if delete == True:
        sleep(delete_pause)
        _os.remove(_os.path.realpath(name_html))