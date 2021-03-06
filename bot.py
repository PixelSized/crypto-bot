# Raw Package
import numpy as np
import pandas as pd
import time as time
#Data Source
import yfinance as yf
#Data viz
import plotly.graph_objs as go

#Reading data from config file
import config as cfg

# Display and server
import dash
import dash_core_components as dcc
import dash_html_components as html



#Storing data from config file
coin = cfg.data["coin"]
period = cfg.data["period"]
interval = cfg.data["interval"]
theme = cfg.data["theme"]

#Creating a function to run during runtime
def runtime():
    #Importing market data
    data = yf.download(
        # tickers list or string as well
        tickers = coin,

        # use "period" instead of start/end
        period = period,

        # fetch data by interval (including intraday if period < 60 days)
        interval = interval,

        # group by ticker
        group_by = 'ticker',

        # adjust all OHLC automatically
        auto_adjust = True,

        # download pre/post regular market hours data
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        threads = True,

        # proxy URL scheme use use when downloading?
        proxy = None
        )

    #Adding Moving average calculated field
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA20'] = data['Close'].rolling(20).mean()

    #Does what it says
    def get_current_price(symbol):
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        return todays_data['Close'][0]

    value = get_current_price(coin)

    #Printing Collected Values
    print(f"Value: {value}")
    print(f"MA5: {data['MA5'].tail(1).item()}")
    print(f"MA20: {data['MA20'].tail(1).item()}")

    #declare figure
    fig = go.Figure(
        layout=go.Layout(
            title=f"{coin} price is {value}"
        )
    )

    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name = 'market data'))
    fig.update_traces(line_width=2, selector=dict(type='candlestick'))

    #Add Moving average on the graph
    fig.add_trace(go.Scatter(x=data.index, y= data['MA20'],line=dict(color='blue', width=2), name = 'Long Term MA'))
    fig.add_trace(go.Scatter(x=data.index, y= data['MA5'],line=dict(color='orange', width=2), name = 'Short Term MA'))

    #Updating X/Y axis and graph
    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=6, label="6h", step="hour", stepmode="backward"),
                dict(count=12, label="12h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=5, label="5d", step="day", stepmode="backward"),
                dict(count=7, label="WTD", step="day", stepmode="todate"),
            ])
        ),
        color="white"
    )
    # Y-Axes
    fig.update_yaxes(
        fixedrange=False,
        autorange=True,
        color="white"
    )


    #Design tingz
    fig.update_layout(
        template=theme,
        font_color="black",
        title_font_color="white",
        legend_title="Legend",
        legend_title_font_color="white",
        legend_font_color="white"
    )

    #Finally show the graph
    #fig.show()  #Old Method

    # Start server through dash
    app = dash.Dash()
    # HTML Tamperment
    app.layout = html.Div([
        dcc.Graph(style={'width': '100vh%', 'height': '98vh'}, figure=fig)
    ])

    app.run_server(debug=True, use_reloader=True, port=8050)  # Turn off reloader if inside Jupyter
    time.sleep(cfg.data["refresh"])   

#I hate how python does this, however run the function DOWN THE BOTTOM ????
runtime()
