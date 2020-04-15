import streamlit as st
import pandas as pd
import seaborn as sns 

def sidebar_configs():
    st.sidebar.title("Style configurations")
    style = st.sidebar.selectbox("Chose a seaborn grid: ", ("darkgrid", "whitegrid", "dark", "white", "ticks"))
    sns.set_style(style)

def plot_graph(df):
        graph = st.selectbox("Chose the graph: ", ("Select", "Bar", "Histogram", "Scatter", "Heatmap"))
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

def drop_useless_columns(df):
    columns = st.multiselect("Chose the columns", df.columns)
    button = st.button("Drop")
    if button:
        new_df = df.drop(columns, axis = 1)
        st.markdown("New dataset")
        st.dataframe(new_df)
        return new_df

def complet_missing_data(df):
    select_method = st.selectbox("Chose the method: ", ("Select", "Mean", "Median", "Mode"))
    if(select_method == "Mean"): 
        columns =  st.multiselect("Chose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].mean())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.dataframe(values_explore)
        
    if(select_method == "Median"): 
        columns =  st.multiselect("Chose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].median())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.dataframe(values_explore)
    
    if(select_method == "Mode"): 
        columns =  st.multiselect("Chose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].mode())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.dataframe(values_explore)

def main():
    sidebar_configs()
    st.title("Analyzing data with Streamlit")
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
        checkbox_flag = st.checkbox("Plot a graph") 
        if(checkbox_flag):
            plot_graph(df)

        st.subheader("Drop useles columns")
        drop_flag = st.checkbox("Drop columns")
        if(drop_flag):
            new_df = drop_useless_columns(df) 
        else:
            new_df = df
        
        st.subheader("Complete missing data")
        complete_flag = st.checkbox("Complete columns")
        if(complete_flag):
            complet_missing_data(new_df)        


if __name__ == "__main__":
    main()