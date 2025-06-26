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

df=pd.read_csv(r"C:\Users\HP\Desktop\Coding\Python\StreamLit\Project\student_habits_performance.csv")

#Data Cleansing
df.dropna(inplace=True)
df.drop(["student_id"],axis=1, inplace=True)
df.drop_duplicates()
df = df.dropna(subset=['gender', 'social_media_hours', 'internet_quality', 'attendance_percentage'])


#dimensions
col1, =st.columns(1)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"{uploaded_file.name} is successfully uploaded")
    st.divider()

    st.title("Important insights about the dataset")

    desc = df.describe()
    st.write(desc)
    st.divider()

    count_female = df[df['gender'] == 'Female'].shape[0]
    count_male = df[df['gender'] == 'Male'].shape[0]
    count_female_job = df[(df['gender'] == 'Female') & (df['part_time_job'] == 'Yes')].shape[0]
    count_male_job = df[(df['gender'] == 'Male') & (df['part_time_job'] == 'Yes')].shape[0]

    gradeA_female= df[(df['gender']=='Female') & (df['exam_score']>=80)].shape[0]
    gradeA_male= df[(df['gender']=='Male') & (df['exam_score']>=80)].shape[0]

    avg_exer_freq = df.groupby('age')['exercise_frequency'].mean().reset_index()


    col1, = st.columns(1)  # Define col1 here before the function

    with col1:
        def stream_data():

            yield f"Total Female: {count_female}" 
            yield f"Total Male: {count_male}"           
            yield f"Total employed females: {count_female_job}"            
            yield f"Total Employed Males: {count_male_job}"

        def stream_data2():

             yield f"Female A grade holders (more than or equal to 80 marks): {gradeA_female}"
             yield f"Male A grade holders (more than or equal to 80 marks): {gradeA_male}"


        with st.expander("Table Details"):
            col2, col3=st.columns(2)
            with col2:
                for line in stream_data():
                    st.write(line)

            with col3:
                 for line in stream_data2():
                      st.write(line)
        st.divider()

        col1, col2, col3=st.columns(3, gap="large")

        with col1:
            options=st.radio("What Plot do you want to see?",
                            ["Pie Chart", "Bar Plot", "TreeMap"],
                            index=0)
        

        if options=="Pie Chart":
            with col2:
                    fig1=px.pie(df,
                                values=[count_female_job, count_male_job],
                                title="Gender Wise Employment Chart")
                    fig1.update_layout(height=400, margin= dict(t=50, b=50))
                    st.plotly_chart(fig1, use_container_width=True)

            with col3:
                 fig2=px.pie(df,
                             values=[gradeA_female, gradeA_male],
                             title="Grade A Student Gender Wise Plot"
                             )
                 fig2.update_layout(height=400, margin= dict(t=50, b=50))
                 st.plotly_chart(fig2, use_container_width=True)

        elif options=="Bar Plot":
             fig1= px.bar(avg_exer_freq, x='age', y='exercise_frequency', color='exercise_frequency', title="Age Wise Average Exercise Frequency Plot", height=600)
             st.plotly_chart(fig1, use_container_width=True)

        else:
             fig1=px.treemap(df, path=['age','gender', 'attendance_percentage'], title="Age vs Gender and Attendance Percentage TreeMap Plot", height=800)


             fig1.update_traces(
                root_color="lightgrey",
            )

             st.plotly_chart(fig1, use_container_width=True)




else:
    st.warning("Please Upload a File")
    st.download_button(
        "Download the required dataset",
        mime="text/csv",
        file_name="data2.csv",
        icon=":material/download:",
        data=df.to_csv().encode("utf-8"),
        type="primary"
    )
