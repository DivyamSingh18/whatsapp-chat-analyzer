import streamlit as st
import preprocessing , funcs
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import plotly.express as px
import seaborn as sns
import pandas as pd

st.sidebar.title('Whatsapp Chat Analyzer')

placeholder = st.title('Please Enter path for whatsapp exported chat.txt file for Data Analysis')
note = st.caption('CAUTION: THIS APPLICATION WORKS FOR THE CHATS EXTRACTED FROM THE 12 HOUR FORMAT PHONES.') 

uploaded_file = st.sidebar.file_uploader('Choose a file')
# st.write(uploaded_file)
# dataframe = pd.read_csv(uploaded_file)
# st.write(dataframe)

# text_input = st.sidebar.text_input("Please, Enter your File Path 👇")
# st.sidebar.caption('For eg. ur/file/path/filename.txt')
# if text_input == '':
#     st.title('')
# elif text_input:
#     st.write('File Path Entered `%s`' % text_input)

#-----------------------------------github code------------------------------------------------------------
# import streamlit as st
# from filepicker import st_file_selector
# os_path = st_file_selector(st, key = 'tif', label = 'Choose tif file')
#-----------------------------------------------------------------------------------------------


# filename = file_selector()

if uploaded_file is not None:
    placeholder.empty()
    # to read file as bytes:
    bytes_data = uploaded_file.getvalue()  # get data from file in the form of bytes 
    data = bytes_data.decode('utf-8')  # decoding the data 
    # filename = uploaded_file.name
    # filename= uploaded_file.name
    # path =os.path.basename(filename)

    df =  preprocessing.PreProcess(data) 

    #printing the data from the file on web app
    st.text('Your Whatsapp Data Looks Like:')
    st.dataframe(df) 

    Authors  = df['Author'].unique().tolist()  
    Authors.sort()
    Authors.insert(0,'Overall')
    
    selected_author = st.sidebar.selectbox('Show Analysis wrt ',Authors)

    if st.sidebar.button('Show Analysis'):
        
        no_of_mgs , no_of_words , no_of_media_msg , no_of_links , no_of_emojis , words_per_msg =  funcs.fetch_stats(selected_author, df)

        col1, col2, col3  = st.columns([0.2, 0.2, 0.2])
    
        with col1:
            st.header ('Total Messages:')
            st.subheader(no_of_mgs)
        with col2:
            st.header ('Total Words:')
            st.subheader(no_of_words)
        with col3:
            st.header('Media Shared:')
            st.subheader(no_of_media_msg)
        
        col4, col5, col6  = st.columns([0.2, 0.2, 0.2])
        with col4:
            st.header('Links Shared:')
            st.subheader(no_of_links)
        with col5:
            st.header('avg Words/txt:')
            st.subheader(words_per_msg)
        with col6:
            st.header('Emojis Shared:')
            st.subheader(no_of_emojis)
      
        components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)
        
    # finding the most active authors in the group/chat  (group bevel analysis)
    
    if selected_author == 'Overall':
        st.title('Most Active Users:')
        x , result_df = funcs.fetch_most_active_users(df)
        fig, ax = plt.subplots()
        col1 , col2 = st.columns(2)

        with col1:
            ax.bar(x.index , x.values,color= 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(result_df)
    
    # creating the wordcloud
    st.title('WordCloud graph for: '+str(selected_author))
    try:
        df_wc  = funcs.create_wordcoud(selected_author,df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig) 
    except Exception as e:
        st.title('Error: '+str(e))

    # Most common words dataframe
    st.title('The Most Common words for: '+str(selected_author))
    _20_most_common_wrds , _100_most_common_wrds = funcs.most_common_words(selected_author,df)

    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        st.dataframe(_100_most_common_wrds)

    with col2:
        fig,ax = plt.subplots()
        ax.barh(_20_most_common_wrds['Word'], _20_most_common_wrds["Times Repeated"],color='#cae00d')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
    # emoji analysis 
    st.title('Emoji Analysis: '+str(selected_author))
    
    try:

        emoji_df = funcs.emoji_analysis(selected_author,df)
        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = px.pie(emoji_df, values='Times Repeated', names='Emoji')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.write(fig)
    except Exception as e:
        st.caption(e)
        st.header("Can't make pie chart : There are no Emojis for this Field.")

    # monthly timeline
    st.subheader('Monthly Activity (Messages per Month)')
    timeline = funcs.monthly_timeline(selected_author,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['Message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig) 

    #daily timeline
    st.subheader('Daily Activity (Messages per Day)')
    daily_timeline =funcs.daily_timeline(selected_author,df)
    fig,ax = plt.subplots()
    ax.plot(daily_timeline['Date'],daily_timeline['Message'], color='#cae00d')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #weekly activity 
    col1, col2 = st.columns(2)

    with col1:
        st.header('Most Active Days')
        weekly_acti = funcs.week_activity_map(selected_author,df)
        fig,ax = plt.subplots()
        ax.bar(weekly_acti.index,weekly_acti.values, color='hotpink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header('Most Active Months')
        monthly_acti = funcs.month_activity_map(selected_author,df)
        fig,ax = plt.subplots()
        ax.bar(monthly_acti.index,monthly_acti.values, color='#D1D100')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
    # heatmap for hourly activity
    st.header('Hourly Activity')
    heatmap = funcs.hourly_activity_heatmap(selected_author,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(heatmap ,cmap="Greens")
    st.pyplot(fig)
        











    


   

