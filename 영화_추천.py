import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns 

st.title('2%부족한 영화 추천 시스템')
df_tab,df2_tab=st.tabs(['popular movies','recommand system'])
with df_tab:
    st.subheader('영화 명작 순위(출처 : imdb)')
    df=pd.read_csv('movie_info.csv')
    df=df[df.columns]
    columns=df.columns
    group_by_option=st.selectbox('당신은 영화의 어떤 점에 중점을 두시나요?:',['None']+list(['runtime(min)','imdb_rating','meta_score']))
    if group_by_option=='None':
        st.image('https://cdn.pixabay.com/photo/2019/11/07/20/48/cinema-4609877_1280.jpg')
    else:
        a=df.sort_values(by=group_by_option,ascending=False)
        ranking=st.slider('몇위까지 확인하고 싶으신가요?',1,250,1)
        st.dataframe(a.head(ranking))
with df2_tab:
    st.subheader('당신이 좋아할만한 영화를 추천해드릴 수 있습니다!')
    st.subheader('단 리뷰는 필수인거 아시죠...?^^;')
    target=st.text_input("당신의 id를 입력하세요",)
    try:
        df2=pd.read_csv('movie_totalinfo.csv')
        pvt=df2.pivot_table(index='user_id',columns='name',values='rating').fillna(0)
        user_corr=pvt.T.corr()
        tmp=user_corr.sort_values(by=target,ascending=False)[target]
        a=tmp[tmp < 0.9999]
        filter1=pd.DataFrame(a).reset_index()
        filter2=filter1['user_id'].head(10)
        filter2
        group_by_option2=st.selectbox('누구의 추천을 받고 싶나요?',['None']+list(filter2))
        if group_by_option2:
            u1=set(df2.loc[df2['user_id']==target]['name'])
            u2=set(df2.loc[df2['user_id']==group_by_option2]['name'])

    except:
        ""