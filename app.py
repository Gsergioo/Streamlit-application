import streamlit as st
import pandas as pd
import seaborn as sns 

def sidebar_configs():
    st.sidebar.title("Style configurations")
    style = st.sidebar.selectbox("Chose a seaborn grid: ", ("darkgrid", "whitegrid", "dark", "white", "ticks"))
    sns.set_style(style)

def main():
    sidebar_configs()
    st.title("Analyzing datas with Streamlit")
    st.image("image/image.jpg", use_column_width=True)
    file = st.file_uploader("Upload your file (csv) ", type="csv")
    if file is not None:
        df = pd.read_csv(file)
        st.header("Vizualization and analyze of data")
        num_lines = st.slider("Enter a number of lines to visualize: ", 1, 100)
        st.dataframe(df.head(num_lines))
        st.markdown(f"Number of lines: {df.shape[0]} ")
        st.markdown(f"Number of columns: {df.shape[1]} ")
        st.subheader("Description of dataset: ")
        st.write(df.describe())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.subheader("Info about missing data and data types")
        st.dataframe(values_explore)
        st.subheader("Graphs")
        checkbox_flag = st.checkbox("Plot a graph?") 
        if(checkbox_flag):
            graph = st.selectbox("Chose the graph: ", ("Bar", "Histogram", "Scatter, Heatmap"))
            if(graph == "Bar"):
                columns = st.multiselect("Chose the columns: ", df.columns)
                if(len(columns) == 1):
                    sns.countplot(x= columns[0], data = df)
                    st.pyplot()
                elif(len(columns) > 1):
                    sns.barplot(x=columns[0], y=columns[1], data=df)
                    st.pyplot()
            if(graph == "Histogram"):
                column = st.selectbox("Chose the column: ", df.columns)
                if(column):
                    sns.distplot(df[column])
                    st.pyplot()
            if(graph == "Scatter"):
                columns = st.multiselect("Chose the columns: ", df.columns)
                if(len(columns) > 1):
                    sns.scatterplot(x=columns[0], y=columns[1], data=df)
                    st.pyplot()
            if(graph == "Heatmap"):
                sns.heatmap()
                
                                
                    



if __name__ == "__main__":
    main()