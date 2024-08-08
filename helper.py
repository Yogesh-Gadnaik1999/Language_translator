import torch
from transformers import AutoProcessor, SeamlessM4Tv2Model
import streamlit as st
from io import BytesIO

try: 
    processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
    model = SeamlessM4Tv2Model.from_pretrained("facebook/hf-seamless-m4t-medium")
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

except Exception as e:
    print("Error",e)

def translate_text(English_text, input_language_code, target_language_code):
    print("English_text",English_text)
    # Set the source and target language codes, adjust these codes based on your model's requirements
    src_lang = input_language_code
    tgt_lang = target_language_code
    
    try:
        # Process input
        # This line might need adjustment based on the specifics of your NLP model and processor
        text_inputs = processor(text=English_text, src_lang=src_lang, return_tensors="pt")
        
        # Generate translation
        # Adjust the method to call your model's specific translation or generation function
        output_tokens = model.generate(**text_inputs, tgt_lang=tgt_lang, generate_speech=False)
        
        # Decode the generated tokens to a string
        translated_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    except Exception as e:
        print("Exception occures",e)
        translated_text= ''
    
    return translated_text


def get_language_code(input_language,target_language,LANGUAGES):
     # Get the language code for the selected language
    input_language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(input_language)]

    # Get the language code for the selected language
    target_language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_language)]
    
    return input_language_code,target_language_code


# Convert DataFrame to CSV
def convert_df_to_csv(df):
    data = df.to_csv(index=False).encode('utf-8')
    mime = 'text/csv'
    label = "Download translated data as CSV"

    return data,mime,label

# Convert DataFrame to Excel
def convert_df_to_excel(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    data = buffer.getvalue()
    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    label = "Download translated data as Excel"

    return data,mime,label


def about_application():
    st.markdown("<h1 style='text-align: center; color: gold;'>About Language Translator</h1>", unsafe_allow_html=True)
    st.write()
    st.write()
    st.info("""
        **Welcome to the Multilingual Translator Application!**

        This application offers you the ability to translate text or multiple columns of an Excel/CSV file into various languages. Here are the key features and how to use them:

        1. **Text Translation:**
            - Select your target language from the dropdown menu.
            - Enter the text you wish to translate in the provided text box.
            - Click the "Translate" button to get the translated text instantly displayed below.

        2. **File Translation:**
            - Upload an Excel (.xlsx) or CSV (.csv) file by clicking the "Upload File" button.
            - Once uploaded, you will see a dropdown menu with all the column names from the file.
            - Select the column you wish to translate.
            - Click the "Translate Column" button to translate the selected column into the target language.
            - The translated data will be available for download as a new file.

        3. **Additional Features:**
            - Bulk Translation: Upload and translate large datasets efficiently.
            - Download Translations: Easily download translated text and files for your records.

        We hope you find this application useful for your translation needs"""
        )

def all_languages():
    LANGUAGES = {
        "afr": "Afrikaans",
        "amh": "Amharic",
        "asm": "Assamese",
        "bel": "Belarusian",
        "ben": "Bengali",
        "bos": "Bosnian",
        "bul": "Bulgarian",
        "cat": "Catalan",
        "ceb": "Cebuano",
        "ces": "Czech",
        "cmn": "Chinese",
        "dan": "Danish",
        "deu": "German",
        "ell": "Greek",
        "eng": "English",
        "est": "Estonian",
        "fin": "Finnish",
        "fra": "French",
        "guj": "Gujarati",
        "heb": "Hebrew",
        "hin": "Hindi",
        "hrv": "Croatian",
        "hun": "Hungarian",
        "hye": "Armenian",
        "ind": "Indonesian",
        "isl": "Icelandic",
        "ita": "Italian",
        "jpn": "Japanese",
        "kan": "Kannada",
        "kat": "Georgian",
        "kaz": "Kazakh",
        "khm": "Khmer",
        "kor": "Korean",
        "lvs": "Latvian",
        "lit": "Lithuanian",
        "mkd": "Macedonian",
        "mlt": "Maltese",
        "mar": "Marathi",
        "mya": "Burmese",
        "npi": "Nepali",
        "nld": "Dutch",
        "pan": "Punjabi",
        "pol": "Polish",
        "por": "Portuguese",
        "ron": "Romanian",
        "rus": "Russian",
        "slk": "Slovak",
        "slv": "Slovenian",
        "som": "Somali",
        "spa": "Spanish",
        "srp": "Serbian",
        "swh": "Swahili",
        "swe": "Swedish",
        "tam": "Tamil",
        "tel": "Telugu",
        "tha": "Thai",
        "tur": "Turkish",
        "ukr": "Ukrainian",
        "urd": "Urdu",
        "vie": "Vietnamese",
        "yor": "Yoruba",
        "zul": "Zulu"
    }
    return LANGUAGES


