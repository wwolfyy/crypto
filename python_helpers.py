# function to get price & mktcap from coingecko
def coingecko_get_data_by_id(slug, num_days):

    from datetime import datetime
    import pandas as pd    
    from pycoingecko import CoinGeckoAPI  # Community project. See: https://github.com/man-c/pycoingecko
    cg = CoinGeckoAPI()
    
    tmp = cg.get_coin_market_chart_by_id(slug, vs_currency='USD', days=num_days)    
        
    df_pr = pd.DataFrame(tmp['prices'])
    df_pr.columns = ['date', slug]
    df_pr['date'] = df_pr['date'].div(1000).apply(datetime.fromtimestamp)
    df_pr.set_index('date', inplace=True)
    df_pr.index = pd.DatetimeIndex(df_pr.index.date)
    df_pr = df_pr.loc[~df_pr.index.duplicated(keep='last'), :]      
    
    df_mkt = pd.DataFrame(tmp['market_caps'])
    df_mkt.columns = ['date', slug]
    df_mkt['date'] = df_mkt['date'].div(1000).apply(datetime.fromtimestamp)
    df_mkt.set_index('date', inplace=True)
    df_mkt.index = pd.DatetimeIndex(df_mkt.index.date)
    df_mkt = df_mkt.loc[~df_mkt.index.duplicated(keep='last'), :]  
    
    return df_pr, df_mkt

# produce price & matk cap dataframe of multiple symbols using coingecko data
def coingecko_get_df(slug_list, num_days, min_length):
    import pandas as pd
    from python_helpers import coingecko_get_data_by_id
    M2E_price = pd.DataFrame()
    M2E_mktcap = pd.DataFrame()
    for sym in slug_list:
        df_pr, df_mkt = coingecko_get_data_by_id(sym, num_days)   
        if len(df_pr.dropna()) < min_length: continue
        M2E_price = pd.concat([M2E_price, df_pr], axis=1)      
        M2E_mktcap = pd.concat([M2E_mktcap, df_mkt], axis=1)
    return M2E_price, M2E_mktcap

# function to produce mktcap-weighted index
def produce_mkt_weighted_index(df_mktcap, name):
    assert df_mktcap.dropna().index[0] == df_mktcap.index[0]
    df_idx = df_mktcap.sum(axis=1).div(df_mktcap.sum(axis=1).iloc[0]).to_frame()
    df_idx.columns = [name]
    return df_idx

# function to plot with unified hover line & log button
def plot_log_unif(dataframe, ttl, hmode='x unified'):
    import plotly.express as px
    fig0 = dataframe.plot(title=ttl)
    fig0.update_layout(
        hovermode=hmode, # "x" | "y" | "closest" | False | "x unified" | "y unified"
        updatemenus=[
            dict(
                type = "buttons",
                direction = "left",
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "linear"}],
                        label="LINEAR",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "log"}],
                        label="LOG",
                        method="relayout"
                    )
                ]),
            ),
        ]
    )
    return fig0

# function to get price data from Binance    
def get_ohlc_from_bianace(sym, interval, start_date, end_date):
    '''
    date format: '2021-06-01'
    '''
    import pandas as pd
    from binance.spot import Spot 
    from datetime import datetime
    import time
    
    client = Spot()
    
    start_time = int(time.mktime(datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timetuple())) * 1000
    end_time = int(time.mktime(datetime.strptime(end_date +' 23:59', '%Y-%m-%d %H:%M').timetuple())) * 1000
    
    tmp = pd.DataFrame(client.klines(sym, interval, limit=10000, startTime=start_time, endTime=end_time))
    tmp.columns = ['time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'quote_av', 'trades', 
                   'tb_base_av', 'tb_quote_av', 'ignore']
    tmp['time'] = pd.to_datetime(tmp['time'], unit='ms')    
    tmp = tmp.loc[tmp['ignore']=='0', :].drop(columns=['Close_time'])
             
    return tmp