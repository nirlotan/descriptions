import streamlit as st
import pandas as pd
import re
import gzip
import pickle
import wget

st. set_page_config(layout="wide")

def find_word(text, word_to_find):
    try:
        # Compile a regular expression pattern that matches the word boundary (\b) followed by the word to find
        pattern = re.compile(r'\b{}\b'.format(re.escape(word_to_find)), re.IGNORECASE)

        # Use the findall method to search for all instances of the word in the text
        matches = pattern.findall(text)

        if matches:
            return True
        else:
            return False
    except:
        print(text)


find_word(text="OG mantra : live, laugh, love side note, I make art",
          word_to_find="MANTRA")

@st.cache_data
def load_data():
    proxy_dict = {"https": "http://proxy-chain.intel.com:911"}
    #pd.read_csv("https://www.dropbox.com/scl/fi/6w456gwd5a25vysady106/users_descriptions.pkl.gzip?rlkey=cljn6kmr3og9twhbumqis23os&dl=1")
    wget.download("https://www.dropbox.com/scl/fi/6w456gwd5a25vysady106/users_descriptions.pkl.gzip?rlkey=cljn6kmr3og9twhbumqis23os&dl=1")
    filename = "users_descriptions.pkl.gzip"
    with gzip.open(filename, 'rb') as pickle_file:
        df = pickle.load(pickle_file)

    df['clickable_url'] = df['screen_name'].apply(
        lambda x: f'<a href="http://x.com/{x}" target="_blank">{x}</a>')

    return df


st.title("Twitter users description search")

df = load_data()

with st.form("user_form", clear_on_submit = False):
    col1, col2 = st.columns([3, 1])
    word_to_search = col1.text_input("keyword to search: ", value = "")
    num_of_users = col2.selectbox('Show first # users:', options=[10, 50, 100, 500, 1000], index=0)
    st.caption('We search for the text, case __insensitive__, and we __keep__ any leading/trailing spaces for better filtering.')
    submit_button = st.form_submit_button(label="search")


all_keywords = [word_to_search]

st.write(f"Original data contains {df.shape[0]:,} users")

if submit_button:

    with st.spinner(f'Searching for {word_to_search}...'):
        subset_df = df[df['description'].apply(lambda x: find_word(x, word_to_search))]

    if subset_df.shape[0] == 0:
        st.error(f"No users found with the keyword '{word_to_search}'")
    else:
        st.success(f"Found {subset_df.shape[0]:,} users with the keyword '{word_to_search}' (case insensitive!)")

        st.write(f"Here are the top {num_of_users} users")
        df_to_show = subset_df.head(num_of_users).to_html(escape=False)
        st.write(df_to_show, unsafe_allow_html=True)