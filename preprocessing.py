import regex as re
import pandas as pd

import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


    # take data from the .txt file and split them into Date, Time, Author , Message

def PreProcess(file_path):
    print
    data = []
    with open(file_path, encoding="utf-8") as fp:
        fp.readline()

    
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    data.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDatapoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)

    # creating pandas dataframe 
    df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'])
    

    # Taking time into 24hr format
    df['24hr_Time'] = pd.to_datetime(df['Time']).dt.time
    df['24hr_Time'] = pd.to_datetime(df['24hr_Time'], format='%H:%M:%S')

    # extraction of day, month and year
    df['date'] = df['Date'].dt.date
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()

    # extraction of hrs and minutes 
    df['hour'] = df['24hr_Time'].dt.hour
    df['minute'] = df['24hr_Time'].dt.minute

    # converting 24hr Date-Time into Time
    df['24hr_Time'] = pd.to_datetime(df['24hr_Time']).dt.time

    # Creating csv file for the user
    #df.to_csv('your_chat_data.csv')  # it was created to check dataframe by me

    # dropping NaN values (texts like you added 'username' , etc )
    df.dropna(inplace=True)

    #extracting the emojis
    df['emoji'] = df["Message"].apply(emoji_split_count)

    # Extracting the links
    URLPATTERN = r'(https?://\S+)'
    df['urlcount'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()

    period = []    # creating one hour period 
    for hour in df[['day_name','hour']]['hour']:
            if hour == 23 :
                period.append(str(hour)+"-"+str('00'))
            elif hour == 0:
                period.append(str("00")+"-"+str(hour+1))
            else:
                period.append(str(hour)+"-"+str(hour+1))

    df['hr_period'] = period
    
    print('Preprocessing Completed Successfully')

    return df

def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    pattern_for_24hr_format = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"

    result = re.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
#     s = s.split(":")
    s = s.split(':', 1)  # added😎 
    if len(s)==2:
        return True
    else:
        return False

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author= None
    

    return date, time, author, message

def emoji_split_count(text):
    emoji_list = []
    data = re.findall(r'\X',text)
    for word in data:
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)
    return emoji_list
    



