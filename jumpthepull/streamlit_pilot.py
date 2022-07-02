# import s3fs, os  # not using AWS S3 --> not using s3fs

import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

st.set_page_config(
    page_title="Rug Pull Gauge Dashboard",
    page_icon="✅",
    layout="wide",
)

# --------------------------- read from AWS S3 --------------------------------
# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
# fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo()#(ttl=600)
# def read_csv_s3(filename):
#   with fs.open(filename) as f:
#       return pd.read_csv(f, index_col='datetime', parse_dates=True)      

# content = read_file("jumpthepull/stepn_solana_combined_table.csv")
# df = read_csv_s3("jumpthepull/stepn_solana_combined_table.csv")
# --------------------------------------------- --------------------------------

# get data stream
@st.experimental_memo()#(ttl=600)
def read_csv(filename):
    return pd.read_csv(filename, index_col='datetime')#, parse_dates=True)

df = pd.read_csv("stepn_solana_combined_table.csv")
df.index.name = 'date'


# dashboard title
st.title("STEPN may be pulling the rug in a whole new kind of way.")

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation


with placeholder.container():

    st.markdown("### GST flow")
    fig = px.area(data_frame=df, y="amount", template='plotly', title='GST supply and demand')
    st.plotly_chart(fig, use_container_width=True)

# with placeholder.container():

#     # create two columns for charts
#     plot_gst, plot_gmt = st.columns(2)    
#     with plot_gst:
#         st.markdown("### GST flow")
#         fig = px.area(data_frame=df, y="amount", template='plotly_dark', title='GST supply and demand')
#         st.write(fig)

    # with plot_gmt:
    #     st.markdown("### Second Chart")
    #     fig2 = px.histogram(data_frame=df, x="age_new")
    #     st.write(fig2)

    # st.markdown("### Detailed Data View")
    # st.dataframe(df)
    # time.sleep(1)
