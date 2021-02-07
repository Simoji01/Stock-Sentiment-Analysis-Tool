from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tkinter as tk

def init():
    global tickers,news_tables,vader,window,ent_ticker,ticks,finwiz_url,parsed_news,currentT,vader,columns,currentRow,tickmap,refreshed,windowtitle
    tickmap = {}
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    currentT = 0
    currentRow = 3
    tickers = []
    parsed_news = []
    news_tables = {}
    windowtitle = tk.StringVar

    window = tk.Tk()
    window.title("Ticker Sentiment: Tracker Last Refreshed:NA")
    window.resizable(width=False, height=False)
    vader = SentimentIntensityAnalyzer()
    columns = ['ticker', 'date', 'time', 'headline']
    ticks = tk.StringVar()
    prnt_tick = "Current tickers:"
    ticks.set(prnt_tick)
    frm_entry = tk.Frame(master=window)
    ent_ticker = tk.Entry(master=frm_entry, width=10)
    lbl_temp = tk.Label(master=frm_entry, text="Enter the ticker of the stock you would like to track")
    lbl_tracking = tk.Label(master=frm_entry, textvariable=ticks)


    ent_ticker.grid(row=1, column=1, sticky="e")
    lbl_temp.grid(row=1, column=0, sticky="w")
    lbl_tracking.grid(row=2, column=0, sticky="w")

    btn_convert = tk.Button(
        master=window,
        text=" Track \N{RIGHTWARDS BLACK ARROW}",
        command=(lambda:condition(1))
    )
    btn_Add = tk.Button(
        master=window,text="Add",
        command=(lambda: condition(0))
    )

    frm_entry.grid(row=1, column=0, padx=10)
    btn_convert.grid(row=1, column=2, padx=10, sticky="n")
    btn_Add.grid(row=1,column=1,padx = 5,sticky = "n")

def condition(upd):
    #check if ticker already exists
    tick = ent_ticker.get()
    if(tick in tickmap and upd == 0):
        return
    if(upd == 0):
        var = tk.IntVar
        tick = tick.upper()
        global currentRow
        tickstuff = tk.Checkbutton(window,command=(lambda : alterTick(tick)),text=tick,onvalue = 1,offvalue = 0,variable = var)
        tickstuff.grid(row=currentRow,column= 0,padx =10,sticky="w")
        tickstuff.select()
        tickmap[tick] = tickstuff
        tickers.append(tick)
        currentRow+= 1
    if(upd == 1):
        plt.close()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        window.title("Ticker Sentiment: Tracker Last Refreshed: "+ current_time)
        updateAll()
    window.update()

def alterTick(tick):
    tickers.remove(tick)
    global news_tables,parsed_news
    news_tables = {}
    parsed_news = []
    tickmap[tick].destroy()
    del tickmap[tick]
    plt.close()
    if(len(tickmap) == 1):
        window.update()
    else:
        window.update()
        updateAll()
def tickerText(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for i in s:
        str1 += i + '\n'
    # return string
    return str1

def updateAll():
    for ticker in tickers:
        url = finwiz_url + ticker
        req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
        response = urlopen(req)
        html = BeautifulSoup(response,features="html.parser")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table


    # Iterate through the news
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]
            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])

    # ---------------------------------------------------------------------------------


    parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)
    scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()
    scores_df = pd.DataFrame(scores)
    parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')
    parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date

    # ---------------------------------------------------------------------------------
    plt.rcParams['figure.figsize'] = [10, 6]

    mean_scores = parsed_and_scored_news.groupby(['ticker', 'date']).mean()

    mean_scores = mean_scores.unstack() \
\

    mean_scores = mean_scores.xs('compound', axis="columns").transpose()
    mean_scores.plot(kind='line')
    plt.grid()
    plt.title("Average stock sentiment")
    plt.ylabel("Sentiment")
    plt.show()

def refreshPlot():
    plt.clf()
    for ticker in tickers:
        url = finwiz_url + ticker
        req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
        response = urlopen(req)
        html = BeautifulSoup(response, features="html.parser")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table

    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]
            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])

    # ---------------------------------------------------------------------------------

    parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)

    scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()

    scores_df = pd.DataFrame(scores)

    parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')

    parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date

    # ---------------------------------------------------------------------------------
    plt.rcParams['figure.figsize'] = [10, 6]

    mean_scores = parsed_and_scored_news.groupby(['ticker', 'date']).mean()

    mean_scores = mean_scores.unstack() \
 \
        # G
    mean_scores = mean_scores.xs('compound', axis="columns").transpose()
    mean_scores.plot(kind='line')
    plt.grid()
    plt.title("Average stock sentiment")
    plt.ylabel("Sentiment")

init()
def refreshdata():
    if(len(tickmap) != 0):
        refreshPlot()
        plt.close()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        window.title("Ticker Sentiment: Tracker Last Refreshed: " + current_time)
    window.after(10000,refreshdata)
window.after(10000,refreshdata)
tk.mainloop()