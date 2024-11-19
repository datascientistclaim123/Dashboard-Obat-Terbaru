import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Membaca data dari file Excel
df = pd.read_excel('df_cleaned.xlsx')

# Streamlit App Title
st.title("Dashboard Sebaran Obat di Tiap Rumah Sakit 💊")
# Sidebar Navigation
page = st.sidebar.selectbox("Choose Page:", ["Filter Data", "Grouped Data", "WordCloud Obat"])

small_note = "Author: Dexcel Oswald Otniel"

# Page 1: Filter Data
if page == "Filter Data":
    st.header("Filter Data Table by Treatment Place")

    # Sidebar for Filtering
    selected_treatment_place = st.sidebar.selectbox(
        "Select Treatment Place:",
        options=["All"] + df['TreatmentPlace'].unique().tolist()
    )

   # Apply Filter
    if selected_treatment_place != "All":
        filtered_df = df[df['TreatmentPlace'] == selected_treatment_place]
    else:
        filtered_df = df

    # Pilih hanya kolom yang diinginkan
    filtered_df = filtered_df[['TreatmentPlace','Nama Item Garda Medika', 'Satuan', 'Qty', 'Amount Bill']]

    # Display Filtered Data
    st.subheader("Filtered Data Table")
    st.write(filtered_df)

    # Display Total Records
    st.text(f"Total Records: {len(filtered_df)}")
    st.markdown(small_note)
    
# Page 2: Grouped Data
elif page == "Grouped Data":
    st.header("Grouped Data Table")

    # Filter by Treatment Place
    selected_treatment_place = st.sidebar.selectbox(
        "Filter by Treatment Place:",
        options=["All"] + df['TreatmentPlace'].unique().tolist()
    )

    # Apply Filter for Grouping
    if selected_treatment_place != "All":
        filtered_group_df = df[df['TreatmentPlace'] == selected_treatment_place]
    else:
        filtered_group_df = df

    # Group by 'Nama Item Garda Medika'
    grouped_df = filtered_group_df.groupby('Nama Item Garda Medika').agg(
        Total_Amount_Bill=('Amount Bill', 'sum'),
        Total_Rows=('ClaimNo', 'count')
    ).reset_index()

    # Add 'Harga Satuan' column
    grouped_df['Harga Satuan'] = grouped_df['Total_Amount_Bill'] / grouped_df['Total_Rows']

    # Rearrange columns: "Nama Item Garda Medika", "Harga Satuan", "Total_Amount_Bill", "Total_Rows"
    grouped_df = grouped_df[['Nama Item Garda Medika', 'Harga Satuan', 'Total_Amount_Bill', 'Total_Rows']]

    # Apply style to highlight "Total_Amount_Bill" column
    def highlight_column(column):
        return ['background-color: #FFEB99' if col == 'Total_Amount_Bill' else '' for col in column]

    styled_grouped_df = grouped_df.style.apply(highlight_column, axis=1, subset=['Total_Amount_Bill'])

    # Display Grouped Data
    st.subheader(f"Grouped Data by 'Nama Item Garda Medika' (Filtered by {selected_treatment_place})")
    st.write(grouped_df)
    
    # Calculate and Display the Total 'Amount Bill' for all grouped data
    total_amount_bill = grouped_df['Total_Amount_Bill'].sum()

    # Format total amount bill in Rupiah format
    formatted_total_amount_bill = f"Rp {total_amount_bill:,.0f}".replace(",", ".")

    st.subheader(f"Total Amount Bill for all grouped data: {formatted_total_amount_bill}")
    st.markdown(small_note)
    
# Page 3: WordCloud Obat
elif page == "WordCloud Obat":
    st.header("WordCloud Obat di Tiap Rumah Sakit")

    # Filter by Treatment Place
    selected_treatment_place = st.sidebar.selectbox(
        "Filter by Treatment Place:",
        options=["All"] + df['TreatmentPlace'].unique().tolist()
    )

    # Apply Filter
    if selected_treatment_place != "All":
        filtered_df = df[df['TreatmentPlace'] == selected_treatment_place]
    else:
        filtered_df = df

    # Generate WordCloud
    if not filtered_df.empty:
        st.subheader(f"WordCloud for 'Nama Item Garda Medika' (Filtered by {selected_treatment_place})")
        
        # Create WordCloud
        wordcloud_text = " ".join(filtered_df['Nama Item Garda Medika'].dropna().astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wordcloud_text)
        
        # Display WordCloud
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filter.")

    # Display Total Records
    st.text(f"Total Records: {len(filtered_df)}")
    st.markdown(small_note)
