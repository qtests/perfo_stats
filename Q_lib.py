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


def calc_stats(pnl_file, capital, bmk_ticker="BTC-USD", out_folder = "Reports"):

    # Startegy
    df_data = pd.read_csv(pnl_file)
    df_analysis = pd.DataFrame()
    df_analysis["pnl_with_capital"]  = df_data["PnL"] + capital
    df_analysis["ret"] =  df_analysis["pnl_with_capital"].pct_change()
    df_analysis["Date"] = pd.to_datetime( df_data["Date"] ).apply(lambda d: d.date())
    df_analysis = df_analysis.set_index( pd.DatetimeIndex( df_analysis["Date"] ) )
    
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









