import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns 
#--------------------------- 영화 추천 시스템 -----------------
st.title('2%(?) 모자란 영화 추천 시스템')
df_tab,df2_tab,df3_tab=st.tabs(['popular movies','recommand system','power reviewer'])
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
# -----------------------아이디 입력창------------------------------------------------------------------
with df2_tab:
    st.subheader('당신이 좋아할만한 영화를 추천해드릴 수 있습니다!')
    st.caption('단 리뷰를 안 남겼으면 추천해드릴 수 없어요 ㅜㅜ')
    target=st.text_input("당신의 id를 입력하세요",)
    try:
        df2=pd.read_csv('movie_totalinfo.csv')
        pvt=df2.pivot_table(index='user_id',columns='name',values='rating').fillna(0)
        user_corr=pvt.T.corr()
        tmp=user_corr.sort_values(by=target,ascending=False)[target]
        a=tmp[tmp < 0.9999]
        filter1=pd.DataFrame(a).reset_index()
        filter2=filter1['user_id'].head(10)
        st.caption("당신과 유사한 성격으로 추정되는 아이디를 가져왔어요~~")
        filter2
        
        group_by_option2=st.selectbox('누구의 추천을 받고 싶나요?',['None']+list(filter2))
        if group_by_option2=='None':
            ''
        else:
            u1=set(df2.loc[df2['user_id']==target]['name'])
            u2=set(df2.loc[df2['user_id']==group_by_option2]['name'])
            diff=u2.difference(u1)
            u2_all=df2.loc[df2['user_id']==group_by_option2]
            filtered=u2_all.loc[df2['name'].isin(diff)]
            answer=filtered.sort_values(by='rating',ascending=False).head()['name']
            if answer.empty:
                st.text("추천해드리려고 했더니 이미 다 본 영화시네요 조금 더 발전해서 2%를 채우도록 노력할게요ㅜㅜ")
            else:
                answer

    except:
        ""
    with df3_tab:
        st.caption("다음은 review를 작성한 리뷰어 순위입니다")
        reviewer=df2['user_id'].value_counts()
        reviewer
        review_table=pd.DataFrame(df2['user_id'].value_counts()[:50]).reset_index()
        # target=st.text_input("당신의 id를 입력하세요",)
        # if target in list(review_table['index']):
        #     st.text("당신은 리뷰어 순위 중 ")

        # # st.caption("이 안에 없으시다구요? 더욱 노력하세요")