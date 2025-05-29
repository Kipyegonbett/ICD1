import streamlit as st
import pandas as pd
from io import BytesIO

# Define diagnosis categories and their ranges
diagnosis_ranges = {
    "Certain infectious or parasitic diseases": ("1A00", "1H0Z"),
    "Neoplasms": ("2A00", "2F9Z"),
    "Diseases of the blood or blood-forming organs": ("3A00", "3C0Z"),
    "Diseases of the immune system": ("4A00", "4B4Z"),
    "Endocrine, nutritional or metabolic diseases": ("5A00", "5D46"),
    "Mental, behavioral and neurodevelopmental disorders": ("6A00", "6E8Z"),
    "Sleep-wake disorders": ("7A00", "7B2Z"),
    "Diseases of the nervous system": ("8A00", "8E7Z"),
    "Diseases of the visual system": ("9A00", "9E1Z"),
    "Diseases of the ear or mastoid process": ("AA00", "AC0Z"),
    "Diseases of the circulatory system": ("BA00", "BE2Z"),
    "Diseases of the respiratory system": ("CA00", "CB7Z"),
    "Diseases of the digestive system": ("DA00", "DE2Z"),
    "Diseases of the skin": ("EA00", "EM0Z"),
    "Diseases of the musculoskeletal system or connective tissue": ("FA00", "FC0Z"),
    "Diseases of genitourinary system": ("GA00", "GC8Z"),
    "Conditions related to sexual health": ("HA00", "HA8Z"),
    "Pregnancy, childbirth or puerperium": ("JA00", "JB6Z"),
    "Certain conditions originating in perinatal period": ("KA00", "KD5Z"),
    "Developmental anomalies": ("LA00", "LD9Z"),
    "Symptoms, signs or clinical findings not elsewhere classified": ("MA00", "MH2Y"),
    "Injury, poisoning or certain consequences of external causes": ("NA00", "NF2Z"),
    "External causes of morbidity or mortality": ("PA00", "PL2Z"),
    "Factors influencing health status or contact with health services": ("QA00", "QF4Z"),
    "Codes for special purposes": ("RA00", "RA26"),
    "Supplementary chapter: Traditional medicine conditions (Module 1)": ("SA00", "ST2Z"),
    "Supplementary section for functioning assessment": ("VA00", "VC50"),
    "Extension codes": ("XA0060", "XY9U"),
}

def filter_by_diagnosis(df, start_code, end_code):
    """Filter dataset based on alphanumeric diagnosis code range."""
    return df[df["Diagnosis"].astype(str).apply(lambda x: start_code <= x <= end_code)]

# Streamlit UI
st.title("Diagnosis Code Analyzer")

uploaded_file = st.file_uploader("Upload your dataset file (.xlsx, .csv, .txt)", type=["xlsx", "csv", "txt"])
start_code = st.text_input("Enter the start diagnosis code (e.g., 1A00):").strip().upper()
end_code = st.text_input("Enter the end diagnosis code (e.g., 1H0Z):").strip().upper()

if uploaded_file and start_code and end_code:
    try:
        file_name = uploaded_file.name
        file_content = uploaded_file.getvalue()

        # Read file based on extension
        if file_name.endswith('.xlsx'):
            df = pd.read_excel(BytesIO(file_content), dtype=str)
            st.success(f"Successfully read Excel file with {len(df)} records")
        elif file_name.endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content), dtype=str)
            st.success(f"Successfully read CSV file with {len(df)} records")
        else:  # Assume text file
            text_content = file_content.decode('utf-8')
            diagnoses = [line.strip() for line in text_content.split('\n') if line.strip()]
            df = pd.DataFrame(diagnoses, columns=['Diagnosis'])
            st.success(f"Successfully read text file with {len(df)} records")

        # Find the category name
        category_name = None
        for category, (start, end) in diagnosis_ranges.items():
            if start_code >= start and end_code <= end:
                category_name = category
                break

        # Filter data based on user input
        filtered_df = filter_by_diagnosis(df, start_code, end_code)

        # Display results
        if category_name:
            st.subheader(f"🩺 Category: {category_name}")
        else:
            st.warning("⚠️ Diagnosis code range does not match any predefined category.")

        st.write(f"📊 Number of diagnoses in range {start_code} to {end_code}: {len(filtered_df)}")

        # Provide CSV download option
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Data", csv, "filtered_diagnosis.csv", "text/csv")

    except Exception as e:
        st.error(f"Error: {str(e)}")
