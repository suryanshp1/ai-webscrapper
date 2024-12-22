import streamlit as st
from scrape import scrape_website, scrape_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

st.title("AI Web Scrapper")
url = st.text_input("Enter the URL")

if st.button("Scrape Site"):
    st.write("Scraping website....") 
    result = scrape_website(url)
    
    if result:
        body_content = scrape_body_content(result)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content

        with st.expander("View DOM content"):
            st.text_area("DOM content", cleaned_content, height=300)

    else:
        st.write("Scraping failed")


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse ?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content....")

            dom_chunks = split_dom_content(st.session_state.dom_content, max_length=6000)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)