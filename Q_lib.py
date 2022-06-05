import os
from os.path import join

import quantstats as qs
import yfinance as _yf

import pandas as pd

import pdfkit

# extend pandas functionality with metrics, etc.
qs.extend_pandas()


def download_prices(ticker):
    p = {"period": "max"}
    return _yf.Ticker(ticker).history(**p)['Close']


def get_strategy_data(pnl_file, capital):

    df = pd.read_csv(pnl_file)
    dfa = pd.DataFrame()
    dfa["pnl_with_capital"]  = df["PnL"] + capital
    dfa["ret"] =  dfa["pnl_with_capital"].pct_change()
    dfa["Date"] = pd.to_datetime( df["Date"] ).apply(lambda d: d.date())
    dfa = dfa.set_index( pd.DatetimeIndex( dfa["Date"] ) )

    return (dfa)


def calc_sharpe(pnl_file, capital):

    df_analysis = get_strategy_data(pnl_file, capital)

    sharpe = qs.stats.sharpe(df_analysis["ret"])

    return ( sharpe  )


def calc_stats(pnl_file, capital, bmk_ticker="BTC-USD", out_folder = "Reports"):

    df_analysis = get_strategy_data(pnl_file, capital)
    
    # Benchmark
    bmk = download_prices(bmk_ticker)
    mask_bk = bmk.index.isin( df_analysis.index )
    bmk = bmk[mask_bk]
    
    df_analysis["BMK"] = df_analysis.apply(lambda row: bmk[ pd.to_datetime(row.Date) ], axis=1)
    df_analysis["BMK"] = df_analysis["BMK"].pct_change()

    # Output
    out_file = os.path.basename(pnl_file)[:-4] + "_tearsheet.html"
    qs.reports.html(df_analysis["ret"], df_analysis["BMK"], output=True, 
                        download_filename=join(out_folder, out_file))
    pdfkit.from_file(join(out_folder, out_file), join(out_folder, out_file[:-5] + ".pdf"))

    print(pnl_file + " - Finito!")

    return









