import sys

from Q_lib import calc_stats

# Create report
# https://opensourceoptions.com/blog/how-to-pass-arguments-to-a-python-script-from-the-command-line/

zorro_out = sys.argv[1]
# zorro_out = "./Data/test_report.csv"

# Strategy start capital
try:
    init_capital = sys.argv[2]
except:
    init_capital = 1000 * 1000

calc_stats(zorro_out, init_capital) 








