import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go 

html_title="""
<style>
.title-test{
font-weight: bold;
padding: 5px;
border-radius: 6px;
}
</style>
"""
col0, = st.columns(1)
with col0:
        date=str(datetime.datetime.now().strftime("%B, %Y"))
        st.write(f"Last Updated On: {date}")

uploaded_file= st.file_uploader("Choose a File", type=["csv"])
df1=pd.read_csv(r"C:\Users\HP\Desktop\Coding\Python\StreamLit\Project\Students_Social_Media_Addiction.csv")

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.success(f"{uploaded_file.name} is succesfully uploaded")
    st.divider()

    #Data Cleansing

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.drop(['Student_ID', 'Relationship_Status'], inplace=True, axis=1)
    
    #Setting the Dimensions
    col1, col2=st.columns(2, gap="small")
    col3, =st.columns(1)   

    with col1:

        # PIE CHART -- 1
        count_female=df[ (df['Age'] >=21) & (df['Gender']=="Female") & (df['Academic_Level']=="Graduate")].size
        st.write(f"The total count for Female Graduates of age more than or equal to 21 is: {count_female}")
        count_male= df[ (df['Age'] >=21) & (df['Gender']=="Male") & (df['Academic_Level']=="Graduate")].size
        st.write(f"The total count for Male Graduates of age more than or equal to 21 is: {count_male}")
        comaprison_df=pd.DataFrame({
            "Gender": ["Female", "Male"],
            "Count": [count_female, count_male]
        
        })

        st.title("Pie Chart", anchor=False)

        fig1= px.pie(comaprison_df, names="Gender", 
                     values=[count_female, count_male], 
                     title="Comparison between number of Male and Femaile Graduates")
        st.plotly_chart(fig1, use_container_width=True)

        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=comaprison_df.to_csv().encode("utf-8"),
                    type="primary",
                    key='comparison')
        st.divider()


    #PIE CHART -- 2
    with col2:
        hours_spent = df.groupby('Country')['Avg_Daily_Usage_Hours'].mean().reset_index()
        top_10_hours = hours_spent.sort_values(by='Avg_Daily_Usage_Hours', ascending=False).head(10)
        st.write(f"The Country with most Social Media usage: {top_10_hours['Country'].values[0]}")
        st.write(f"The Country with least Social Media usage: {top_10_hours['Country'].values[-1]} ")

        st.title("Pie Chart", anchor=False)
        fig1=px.pie(top_10_hours, names="Country",
                    values="Avg_Daily_Usage_Hours",
                    title="Avg Hours Spent by top 10 countries in Social Media",)
        st.plotly_chart(fig1, use_container_width=True)

        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=top_10_hours.to_csv().encode("utf-8"),
                    type="primary")
        st.divider()

    
    with col3:

        #BAR GRAPH -- 1

        st.title("Top 10 countries with most number of Teenagers", anchor=False)
        teenagers=df[df['Age']>19].sort_values(by="Age", ascending=False)

        countries= teenagers['Country'].value_counts().reset_index()
        countries.columns=["Country", "Count"]
        

        fig1= px.bar(countries.head(10), x="Country", y="Count")
        st.plotly_chart(fig1, use_container_width=True)

        st.download_button("Get Data",
                           data=countries.to_csv().encode("utf-8"), 
                           file_name="data.csv", 
                           mime="text/csv",
                           type="primary",
                           icon=":material/download:",
                           key="teenagers")
        st.divider()
        
        #TREEMAP

        st.title("Effect of Social Median On Mental Health", anchor=False)

        df['Mental_Health_Score']= df['Mental_Health_Score'].astype(str)
        mental=df.groupby(['Most_Used_Platform', 'Mental_Health_Score', 'Country']).size().reset_index() 
        mental = mental.sort_values('Mental_Health_Score', ascending=False)
 

        fig2=px.treemap(mental,
                        path=['Most_Used_Platform', 'Country', 'Mental_Health_Score'],
                        values='Mental_Health_Score',
                        width=2000,
                        height=1000,
                        color='Mental_Health_Score'
                        )
        fig2.update_traces(
                 hovertemplate=(
                "<b>Path:</b> %{id}<br>"  # shows full hierarchy like Instagram/France/7
                ),
                    textinfo="label"
                )
        st.plotly_chart(fig2, use_container_width=True) 
        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=mental.to_csv().encode("utf-8"),
                    type="primary",
                    key='mental'
                    )
        st.divider()
        
        #BAR GRAPH -- 2

        addiction=df.groupby(by='Addicted_Score')['Most_Used_Platform'].value_counts().unstack().fillna(0)

        fig3=px.bar(addiction, barmode='stack', width=2000, height=800, title='Most Used Platform Vs Addicted Score')
        st.plotly_chart(fig3, use_container_width=True)  

        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=addiction.to_csv().encode("utf-8"),
                    type="primary",
                    key='addiction'
                    )
        st.divider()
        
        #BOX PLOT 
        
        platform_score_table = df.groupby(['Most_Used_Platform', 'Addicted_Score']).size().reset_index(name='Count')
        
        fig4= px.box(df, x='Most_Used_Platform', y='Addicted_Score', color="Most_Used_Platform", title="📊 Platform-wise Addicted Score Table")
        st.plotly_chart(fig4, use_container_width=True)

        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=platform_score_table.to_csv().encode("utf-8"),
                    type="primary",
                    key="Box")
        st.divider()


        #SCATTER PLOT
        st.title('10 Countries With Least Sleep Hours Per Night', anchor=False)
        hours=df.groupby(by='Country')['Sleep_Hours_Per_Night'].mean().reset_index().head(10)
        least_hours=hours.sort_values(by='Sleep_Hours_Per_Night', ascending=True).head(10)

        fig5=go.Figure([
            go.Scatter(
                x=least_hours['Country'],
                y=least_hours['Sleep_Hours_Per_Night'],
                marker=dict(
                size=12,
                color='red',  # Customize marker color
                opacity=0.7
            ),
            mode='markers+lines'
            )
        ])

        st.plotly_chart(fig5, use_container_width=True)
        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=least_hours.to_csv().encode("utf-8"),
                    type="primary",
                    key='hours'
                    )
        st.divider()
        
        #PIE CHART -- 3
        
        st.title("Academic Impact: Yes vs No")
        df.dropna(subset=['Affects_Academic_Performance'], inplace=True)
        req_data= df['Affects_Academic_Performance'].value_counts().reset_index()
        req_data
        fig6= px.pie(req_data, names='Affects_Academic_Performance',
                     values='count',
                     color='Affects_Academic_Performance',
                     title='Pie Chart')
        st.plotly_chart(fig6, use_container_width=True)

        st.download_button("Get Data",
                    mime="text/csv",
                    file_name="data.csv",
                    icon=":material/download:",
                    data=req_data.to_csv().encode("utf-8"),
                    type="primary",
                    key='Yes/No'
                    )
        st.divider()
    
    #CHOLOROPLETH

    fig7 = px.choropleth(
    df, 
    locations='Country',  # name of the column with country names
    locationmode='country names',  # or 'ISO-3' if using 3-letter codes
    color='Avg_Daily_Usage_Hours',  # numeric variable to shade by
    color_continuous_scale='Viridis',  # or 'Blues', 'Reds', etc.
    title='Avg Daily Usage Hours by Country',
    width=2000
    )

    st.plotly_chart(fig7, use_container_width=True)
    st.divider()
    
        
else:
    st.download_button("Download the required dataset",
                    mime="text/csv",
                    file_name="data1.csv",
                    icon=":material/download:",
                    data=df1.to_csv().encode("utf-8"),
                    type="primary")

    st.warning("Please Upload a File")


