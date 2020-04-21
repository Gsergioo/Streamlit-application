import streamlit as st
import pandas as pd
import seaborn as sns 
import base64


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href
def show_basic_infos(df):
    st.header("Basic infos about data")
    num_lines = st.slider("Enter a number of lines to visualize: ", 1, 100)
    st.dataframe(df.head(num_lines))
    st.markdown(f"Number of lines: {df.shape[0]} ")
    st.markdown(f"Number of columns: {df.shape[1]} ")
    values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
    st.subheader("Missing data and data types")
    st.dataframe(values_explore)

def show_descriptive_info(df):
    st.header("Data variance")
    options = list(df.columns)
    options = [x for x in options if(df[x].dtypes != "O" and df[x].dtypes != "str" and df[x].dtypes != "bool")]
    options.append("All")
    columns = st.multiselect("Chose columns: ", options)
    if("All" not in columns and len(columns) > 0):
        options = ("Select", "Mean", "Median", "Standar Deviation", "Quartiles", "Complete Description")
        info = st.selectbox("Chose method: ",options)
        if(info == "Mean"):
            st.markdown("Mean: ")
            st.write(df[columns].mean())
        if(info == "Median"):
            st.markdown("Median: ")
            st.write(df[columns].median())
        if(info == "Standar Deviation"):
            st.markdown("Standard Deviation: ")
            st.write(df[columns].std())
        if(info == "Quartiles"):
            st.markdown("Quartiles: ")
            st.write(df[columns].quantile(q = 0.25))
            st.write(df[columns].quantile(q = 0.50))
            st.write(df[columns].quantile(q = 0.75))
        if(info == "Complete Description"):
            st.markdown("Description: ")
            st.write(df[columns].describe())
    else:
        info = st.selectbox("Chose method: ", ("Select", "Mean", "Median", "Standar Deviation", "Quartiles", "Complete Description"))
        if(info == "Mean"):
            st.markdown("Mean: ")
            st.write(df.mean())
        if(info == "Median"):
            st.markdown("Median: ")
            st.write(df.median())
        if(info == "Standar Deviation"):
            st.markdown("Standard Deviation: ")
            st.write(df.std())
        if(info == "Quartiles"):
            st.markdown("Quartiles: ")
            st.write(df.quantile(q = 0.25))
            st.write(df.quantile(q = 0.5))
            st.write(df.quantile(q = 0.75))
        if(info == "Complete Description"):
            st.markdown("Description: ")
            st.write(df.describe())

def sidebar_configs():
    st.sidebar.title("Let's go!")
    data_option = st.sidebar.selectbox("Chose dataset: ", ("Load file", "Use example"))
    if(data_option == "Load file"):
        file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    if(file is not None):
        df = pd.read_csv(file)
        st.sidebar.subheader("Style configuration")
        style = st.sidebar.selectbox("Chose a seaborn grid: ", ("darkgrid", "whitegrid", "dark", "white", "ticks"))
        sns.set_style(style)

        basic_infos = st.sidebar.checkbox("Informações básicas")
        if(basic_infos):
            show_basic_infos(df)

        univariate_info = st.sidebar.checkbox("Informações descritivas")
        if(univariate_info):
            show_descriptive_info(df)    

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


def complet_missing_data(df):
    select_method = st.selectbox("Chose the method: ", ("Mean", "Median", "Mode"))
    if(select_method == "Mean"): 
        columns =  st.multiselect("Chose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].mean())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.dataframe(values_explore)
        return df
        
    if(select_method == "Median"): 
        columns =  st.multiselect("Chose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].median())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.dataframe(values_explore)
        return df 
      
    if(select_method == "Mode"): 
        columns =  st.multiselect("Chose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].mode())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.dataframe(values_explore)
        return df

def main():
    st.title("Analyzing data with Streamlit")
    st.image("image/image.jpg", use_column_width=True)
    sidebar_configs()

if __name__ == "__main__":
    main()