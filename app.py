import streamlit as st
import pandas as pd
from helper import translate_text,all_languages,get_language_code,about_application,convert_df_to_csv,convert_df_to_excel
from datetime import datetime
from PIL import Image
from io import BytesIO

def main():
    # Load your image
    image = Image.open('D:\Translator_POC\image.png')

    # Create two columns
    col1, col2 = st.columns([1, 5]) 

    with col1:
        st.image(image, use_column_width=True)

    # Display the title in the second column
    with col2:  
        st.markdown("<h1 style='color: gold;'>Language Translator</h1>", unsafe_allow_html=True)

    LANGUAGES=all_languages()

    language_options = ["Choose language"] + list(LANGUAGES.values())

    input_language = st.selectbox(
        "Select the language of the text you want to translate:",
        language_options
    )

    # Dropdown for selecting the target language
    target_language = st.selectbox(
        "Select the language you want to translate to:",
        language_options
    )

    # User can either enter text manually or upload a file
    input_option = st.radio("Choose an input method:", ("Enter text manually", "Upload file (Excel/CSV)"))

    english_text = ""
    file_uploaded = None
    columns_to_translate = []

    if input_option == "Enter text manually":
        # Text area for input English sentences
        english_text = st.text_area("Enter text here:")
    else:
        # File uploader for Excel/CSV files
        file_uploaded = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])
        if file_uploaded is not None:
            try:
                if file_uploaded.name.endswith('.csv'):
                    df = pd.read_csv(file_uploaded)
                else:
                    df = pd.read_excel(file_uploaded)

                # Display the column names in a multiselect box
                columns_to_translate = st.multiselect("Select the columns to translate:", df.columns)
            except Exception as e:
                st.error(f"Error reading file: {e}")

    # Button to trigger translation
    if st.button("Translate"):
        start_time = datetime.now()
        st.write(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("Translation process is started...!")

        if input_option == "Enter text manually":
            if english_text:
                if input_language == "Choose language" or target_language == "Choose language":
                        st.write("Please select both the input and target languages.")
                else:
                    input_language_code,target_language_code=get_language_code(input_language,target_language,LANGUAGES)
                    
                    # Translate the text
                    translated_text = translate_text(english_text, input_language_code, target_language_code)
                    
                    # Display the original and translated text in two columns
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_area("Original English text:", english_text, height=200)
                    with col2:
                        st.text_area("Translated text:", translated_text, height=200)
            else:
                st.warning("Please enter some text to translate.")
        else:
            if file_uploaded is not None and columns_to_translate:
                try:
                    if input_language == "Choose language" or target_language == "Choose language":
                        st.write("Please select both the input and target languages.")
                    else:
                        input_language_code,target_language_code=get_language_code(input_language,target_language,LANGUAGES)
                    
                        # Translate the selected columns
                        for column in columns_to_translate:
                            translated_column_name = f"Translated_{column}"
                            df[translated_column_name] = df[column].apply(
                                lambda x: translate_text(str(x), input_language_code, target_language_code)
                            )

                        # st.write("Translated Data")
                        # st.markdown("<p style='color: gold;'>Translated Data</p>", unsafe_allow_html=True)
                        # st.write(df.head(5))
                        
                        
                        # file_name = f"Translated_{file_uploaded.name}"
                        
                        # data=df.to_csv(index=False).encode('utf-8')
                        # st.download_button(
                        #     label="Download translated data as CSV",
                        #     data=data,
                        #     file_name=file_name,
                        #     mime='text/csv',
                        # )
                        
                        st.session_state.translated_df = df
                        end_time = datetime.now()
                        st.write(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        st.write(f"Duration: {end_time - start_time}")

                except Exception as e:
                    st.error(f"Error during translation: {e}")
            else:
                st.warning("Please upload a file and select columns to translate.")


    if 'translated_df' in st.session_state:
        file_name = f"Translated_{file_uploaded.name}"
        df = st.session_state.translated_df

        st.markdown("<p style='color: gold;'>Translated Data</p>", unsafe_allow_html=True)
        st.write(df.head(5))

        download_option = st.radio("Choose a filetype to download:", ("Download as CSV", "Download as Excel"))

        if download_option == 'Download as CSV':
            data,mime,label=convert_df_to_csv(df)
            file_name = f'{file_name}.csv'

        elif download_option == 'Download as Excel':
            data,mime,label=convert_df_to_excel(df)
            file_name = f'{file_name}.xlsx'


        if 'data' in locals():
            st.download_button(
                label=label,
                data=data,
                file_name=file_name,
                mime=mime
            )
    
st.sidebar.markdown("""
    <style>
    .sidebar-title {
        color: #FF6347; /* Tomato */
        font-size: 24px;
        font-weight: bold;
        text-align: center; /* Center the text */
    }
    </style>
    <div class="sidebar-title">Menu</div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

#For select box
# page = st.sidebar.selectbox("Choose a page", ["Home", "About Application"])

# if page == "Home":
#     main()
    
# elif page == "About Application":
#     about_application()

# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Create hyperlinks for navigation in the sidebar
if st.sidebar.button("Home"):
    st.session_state.page = 'Home'
if st.sidebar.button("About App"):
    st.session_state.page = 'AboutApplication'

# Conditional rendering based on the session state
if st.session_state.page == 'Home':
    main()
elif st.session_state.page == 'AboutApplication':
    about_application()
    