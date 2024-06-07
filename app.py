import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

st.title('Interactive Data Visualization Dashboard')

# Step 1: File uploader for CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Step 2: Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Step 3: Display the dataframe
    st.write("DataFrame:")
    st.write(df)

    # Step 4: Display basic statistics
    st.write("Basic Statistics:")
    st.write(df.describe())

    # Step 5: Data visualization
    st.write("Data Visualization:")

    # Select the type of plot
    plot_type = st.selectbox("Select Plot Type:",
                             ["Scatter Plot", "Histogram", "Pair Plot", "Correlation Matrix", "Box Plot"])

    if plot_type == "Scatter Plot":
        # Select columns for scatter plot
        selected_x = st.selectbox("Select X-axis:", df.columns)
        selected_y = st.selectbox("Select Y-axis:", df.columns)
        color_by = st.selectbox("Color By:", [None] + list(df.columns))
        size_by = st.selectbox("Size By:", [None] + list(df.columns))

        if selected_x and selected_y:
            # Create and display the scatter plot
            fig, ax = plt.subplots()
            sns.scatterplot(x=selected_x, y=selected_y, hue=color_by, size=size_by, data=df, ax=ax)
            st.pyplot(fig)

    elif plot_type == "Histogram":
        # Select column for histogram
        selected_column = st.selectbox("Select Column:", df.columns)

        if selected_column:
            # Create and display the histogram
            fig, ax = plt.subplots()
            sns.histplot(df[selected_column], kde=True, ax=ax)
            st.pyplot(fig)

    elif plot_type == "Pair Plot":
        # Select columns for pair plot (multi-select)
        selected_columns = st.multiselect("Select Columns:", df.columns)

        if selected_columns:
            # Create and display the pair plot
            fig = sns.pairplot(df[selected_columns])
            st.pyplot(fig)

    elif plot_type == "Correlation Matrix":
        # Calculate correlation matrix
        corr_matrix = df.corr()

        # Create and display the heatmap
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    elif plot_type == "Box Plot":
        # Select column for box plot
        selected_column = st.selectbox("Select Column:", df.columns)

        if selected_column:
            # Create and display the box plot
            fig, ax = plt.subplots()
            sns.boxplot(y=df[selected_column], ax=ax)
            st.pyplot(fig)

    # Step 6: Download processed data
    st.write("Download Processed Data:")
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label="Download CSV",
        data=buffer,
        file_name="processed_data.csv",
        mime="text/csv"
    )
