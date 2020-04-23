import streamlit as st
import pandas as pd
import seaborn as sns 
import base64
import matplotlib.pyplot as plt

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
        info = st.selectbox("Choose method: ", ("Select", "Mean", "Median", "Standar Deviation", "Quartiles", "Complete Description"))
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

def show_correlations_info(df):
    st.header("Data correlations")
    options = [x for x in df.columns if(df[x].dtypes != "O" and df[x].dtypes != "str" and df[x].dtypes != "bool")]
    columns = st.multiselect("Select columns: ", options)
    correlation_type = st.selectbox("Choose correlation type: ", ("Select", "Pearson", "Spearman"))
    if(columns is not None):
        if(correlation_type == "Pearson"):
            st.markdown("Correlation: ")
            st.write(df[columns].corr(method = "pearson"))

        if(correlation_type == "Spearman"):
            st.markdown("Correlation: ")
            st.write(df[columns].corr(method = "spearman"))
        
def plot_graph(df):
        graph = st.selectbox("Choose the graph: ", ("Select", "Bar", "Histogram", "Scatter", "Heatmap"))
        if(graph == "Bar"):
            columns = st.multiselect("Chose the columns: ", df.columns)
            if(len(columns) == 1):
                sns.countplot(x= columns[0], data = df)
                st.pyplot()
            elif(len(columns) > 1):
                sns.barplot(x=columns[0], y=columns[1], data=df)
                st.pyplot()
        if(graph == "Histogram"):
            column = st.selectbox("Choose the column: ", df.columns)
            bins = st.slider("Select a number of bins: ", 1, 100)
            if(column):
                sns.distplot(df[column], bins = bins)
                st.pyplot()
        if(graph == "Scatter"):
            columns = st.multiselect("Choose the columns: ", df.columns)
            if(len(columns) > 1):
                sns.scatterplot(x=columns[0], y=columns[1], data=df)
                st.pyplot()
        if(graph == "Heatmap"):
            options = [x for x in df.columns if(df[x].dtypes != "O" and df[x].dtypes != "str" and df[x].dtypes != "bool")]
            plt.figure(figsize=(14,12))
            sns.heatmap(df.corr())
            st.pyplot()


def complet_missing_data(df):
    select_method = st.selectbox("Choose the method: ", ("Mean", "Median", "Mode"))
    if(select_method == "Mean"): 
        columns =  st.multiselect("Choose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].mean())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.markdown("New dataset: ")
        st.dataframe(values_explore)
        return df
        
    if(select_method == "Median"): 
        columns =  st.multiselect("Choose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].median())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.markdown("New dataset: ")
        st.dataframe(values_explore)
        return df 
      
    if(select_method == "Mode"): 
        columns =  st.multiselect("Choose the columns: ", df.columns)
        for column in columns:
            df[column] = df[column].fillna(df[column].mode())
        values_explore = pd.DataFrame({"Column": df.columns, "Types": df.dtypes, "NA #": df.isna().sum(), "NA %": df.isna().sum()/df.shape[0] * 100})
        st.markdown("New dataset: ")
        st.dataframe(values_explore)
        return df

def sidebar_configs():
    df = None
    st.sidebar.title("Let's go!")
    data_option = st.sidebar.selectbox("Choose dataset: ", ("Load file", "Use example (iris dataset)"))
    if(data_option == "Load file"):
        file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        if(file is not None):
            df = pd.read_csv(file)
    else:
        df = pd.read_csv("dataset/iris.csv")
    if(df is not None):
        style = st.sidebar.selectbox("Choose a seaborn grid: ", ("darkgrid", "whitegrid", "dark", "white", "ticks"))
        sns.set_style(style)

        basic_infos = st.sidebar.checkbox("Basic infos")
        if(basic_infos):
            show_basic_infos(df)

        univariate_info = st.sidebar.checkbox("Descriptive infos")
        if(univariate_info):
            show_descriptive_info(df)    
        
        correlations_info = st.sidebar.checkbox("Correlation infos")
        if(correlations_info):
            show_correlations_info(df)
        
        plot_graph_flag = st.sidebar.checkbox("Plot graphs")
        if(plot_graph_flag):
            plot_graph(df)

        complete_data = st.sidebar.checkbox("Complete missing data: ")
        if(complete_data):
            new_df = complet_missing_data(df)
            st.write(f"Download new dataset: {get_table_download_link(new_df)}", unsafe_allow_html=True)

        

def main():
    st.title("Analyzing data with Streamlit")
    st.image("image/image.jpg", use_column_width=True)
    sidebar_configs()
    st.write("Desenvolvido no aceleradev da Codenation")

if __name__ == "__main__":
    main()