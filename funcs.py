import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import streamlit as st
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_author, df):    
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author

    # total no of messages
    no_of_msgs = df.shape[0]   

    # total no of words
    Total_words = []
    for msg in df['Message']:
        Total_words.extend(msg.split())
    no_of_words = len(Total_words)     

    # total no of media messages 
    no_of_media_msg = df[df['Message'] == '<Media omitted>'].shape[0]  

    # extracting total urls 
    URLPATTERN = r'(https?://\S+)'
    df['urlcount'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
    no_of_links = np.sum(df.urlcount)

    # Extracting the no of emojis 
    no_of_emojis = sum(df['emoji'].str.len())
    
    # no of words per message
    
    words_per_msg = np.round(no_of_words / df.shape[0],2)  # words per msg 
    

    return no_of_msgs, no_of_words , no_of_media_msg , no_of_links ,no_of_emojis , words_per_msg

def fetch_most_active_users(df):
    x = df['Author'].value_counts().head()
    name = x.index
    count = x.values

    # percentage of messages  
    result_df1 = round((df['Author'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','Author':'Percentage'} )
    result_df2 =df['Author'].value_counts().reset_index().drop('index',axis=1).rename(columns={'Author':'No. of Msgs'} )
    result_df = pd.concat([result_df1, result_df2], axis=1, join="inner")

    return x , result_df

def create_wordcoud(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    df_media_removed = df[df['Message'] != '<Media omitted>']
    wc = WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    df_wc = wc.generate(df_media_removed["Message"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    df_media_removed = df[df['Message'] != '<Media omitted>']
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    words =[]   # empty list for most common words
    for msg in df_media_removed['Message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    
    # create dataframe for most common
    result_df20 = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0:'Word', 1 :"Times Repeated"})
    result_df100 = pd.DataFrame(Counter(words).most_common(100)).rename(columns={0:'Word', 1 :"Times Repeated"})
    return result_df20,  result_df100
    
def emoji_analysis(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    emojis = []
    for msg in df['Message']:
        emojis.extend([c for c in msg if  c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0:'Emoji', 1 :"Times Repeated"})
    return emoji_df

def monthly_timeline(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    timeline = df.groupby(['year','month','month_num']).count()['Message'].reset_index()
    time= []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+ str(timeline['year'][i]))
    timeline['time'] = time
    timeline = timeline.sort_values(['year','month_num']).reset_index()
    return timeline

def daily_timeline(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    daily_timeline = df.groupby('Date').count()['Message'].reset_index()
    return daily_timeline

def week_activity_map(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    weekly_acti = df['day_name'].value_counts()    # activity per day 
    return weekly_acti

def month_activity_map(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    monthly_acti = df['month'].value_counts()    # activity per month 
    return monthly_acti

def hourly_activity_heatmap(selected_author,df):
    if selected_author != 'Overall':
        df = df[df["Author"] == selected_author]  # taking the df of the selected_author
    heatmap = df.pivot_table(index='day_name',columns='hr_period',values='Message',aggfunc='count').fillna(0)
    return heatmap

        

    







   