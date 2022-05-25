import sys
from glob    import glob
from os.path import join

from Q_lib import calc_stats

# Create reports
# https://opensourceoptions.com/blog/how-to-pass-arguments-to-a-python-script-from-the-command-line/

try:
    zorro_out_folder = sys.argv[1]
    # zorro_out = "Data
except:
    zorro_out_folder = "Data"


# Start capital
try:
    init_capital = sys.argv[2]
except:
    init_capital = 1000 * 1000


# BMK
try:
    bmk_ticker = sys.argv[3]
except:
    bmk_ticker = "BTC-USD"


# Get files and process
all_zoro_reports = glob(join(zorro_out_folder, '*.csv'))

for item in all_zoro_reports:
    calc_stats(item, init_capital, bmk_ticker)








