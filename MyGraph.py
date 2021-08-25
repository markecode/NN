from plotly.offline import plot

class MyGraph:
    
    fig = {}
    INCREASING_COLOR = '#17BECF'
    DECREASING_COLOR = '#7F7F7F'
    
    def __init__(self,df,name):  
        df.sort_values(by=['date'], inplace=True, ascending=True)
        data = [
            dict(
                type = 'candlestick',
                open = df.Open,
                high = df.High,
                low = df.Low,
                close = df.Close,
                x = df.date,
                yaxis = 'y2',
                name = name,
                increasing = dict(line = dict(color = self.INCREASING_COLOR)),
                decreasing = dict(line= dict(color = self.DECREASING_COLOR))
            )
        ]
        
        layout = dict()
        self.fig = dict(data = data,layout=layout)
        self.fig['layout'] = dict()
        self.fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'
        self.fig['layout']['xaxis'] = dict( rangeselector = dict( visible = True ) )
        self.fig['layout']['yaxis'] = dict( domain = [0, 0.2], showticklabels = False )
        self.fig['layout']['yaxis2'] = dict( domain = [0.2, 0.8] )
        self.fig['layout']['legend'] = dict( orientation = 'h', y=0.9, x=0.3, yanchor='bottom' )
        self.fig['layout']['margin'] = dict( t=40, b=40, r=40, l=40 )
        
        rangeselector=dict(
            visible = True,
            x = 0, y = 0.9,
            bgcolor = 'rgba(150, 200, 250, 0.4)',
            font = dict( size = 13 ),
            buttons=list([
                dict(count=1,
                     label='reset',
                     step='all'),
                dict(count=1,
                     label='1yr',
                     step='year',
                     stepmode='backward'),
                dict(count=3,
                    label='3 mo',
                    step='month',
                    stepmode='backward'),
                dict(count=1,
                    label='1 mo',
                    step='month',
                    stepmode='backward'),
                dict(step='all')
            ]))
            
        self.fig['layout']['xaxis']['rangeselector'] = rangeselector
        
    def Volume(self,df):        
        colors = []      
        for i in range(len(df.Close)):
            if i != 0:
                if df.Close[i] > df.Close[i-1]:
                    colors.append(self.INCREASING_COLOR)
                else:
                    colors.append(self.DECREASING_COLOR)
            else:
                colors.append(self.DECREASING_COLOR)
                
        self.fig['data'].append( dict( x=df.date, y=df.Volume,                         
                                 marker=dict( color=colors ),
                                 type='bar', yaxis='y', name='Volume' ) )
        
    def Addbar(self,df,name):  
        colors = []          
        for i in range(len(df.StrategyReturn)):
            if i != 0:
                if df.StrategyReturn[i] > 0:
                    colors.append(self.INCREASING_COLOR)
                else:
                    colors.append(self.DECREASING_COLOR)
            else:
                colors.append(self.DECREASING_COLOR)
                
        self.fig['data'].append( dict( x=df.date, y=df.StrategyReturn,                         
                                 marker=dict( color=colors ),
                                 type='bar', yaxis='y', name=name ) )
    def AddLine(self,df,name):        
        self.fig['data'].append( dict( x=df.date, y=df.StrategyReturn, type='scatter',line = dict(width=1),                     
                                 marker=dict( color='#E377C2' ),
                                 yaxis='y', name=name ) )
        
        
    def PlotGraph(self):        
        plot(self.fig, filename='simple_candlestick.html',auto_open = True)

