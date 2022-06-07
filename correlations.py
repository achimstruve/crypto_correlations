import pandas_datareader as web
import matplotlib.pyplot as plt
import mplfinance as mpf
import seaborn as sns
import datetime as dt

plot_heatmap = True

currency = "USD"
metric = "Close"

start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()

crypto = [
    "BTC",
    "ETH",
    "AVAX",
    "MATIC",
    "BNB",
    "ADA",
    "LINK",
    "FTM",
    "DAG",
    "FLUX",
]
colnames = []

first = True
for ticker in crypto:
    data = web.DataReader(f"{ticker}-{currency}", "yahoo", start, end)
    if first:
        combined = data[[metric]].copy()
        colnames.append(ticker)
        combined.columns = colnames
        first = False
    else:
        combined = combined.join(data[metric])
        colnames.append(ticker)
        combined.columns = colnames

if not plot_heatmap:
    # Plot prices on log scale
    plt.yscale("log")
    for ticker in crypto:
        plt.plot(combined[ticker], label=ticker)
    plt.legend(loc="upper right")

if plot_heatmap:
    # calculate correlation
    combined = combined.pct_change().corr(method="pearson")
    sns.heatmap(combined, annot=True, cmap="coolwarm")

plt.show()
