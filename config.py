import preprocessing

data = {
    "coin": "BTC-AUD",  #The Coin we are reading
    "period": "5d", # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max  # (optional, default is '1mo')
    "interval": "5m", # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    "refresh": "300", # this should be the amount of seconds oh whatever the interval is (secs = mins x 60)
    "theme": "plotly_dark" #Available themes: 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'
}


use_anonymous = True
