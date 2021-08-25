from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np

class LinePlot:
    def __init__(self,data1,data2):
        trace = go.Scatter(
            x = np.arange(len(data1)),
            y = data1,
            mode = 'lines',
            name ='Result')
        trace1  = go.Scatter(
                x = np.arange(len(data2)),
                y =data2,
                mode = 'lines',
                name ='Actual Result') 
        data = [trace,trace1]
        plot(data, filename='basic-line.html')

