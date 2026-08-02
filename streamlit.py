#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
from Avyakt_Murli_Assistant import chat

st.set_page_config(
    page_title="AVYAKT MURLI Teaching Assistant",
    page_icon="🎓"
)

st.title("🎓 AVYAKT MURLI Teaching Assistant")

question = st.text_input(
    "Ask a question from the textbook"
)

if st.button("Submit"):

    with st.spinner("Searching textbook..."):

        answer, pages = chat(question)

    st.success("Answer Generated")

    st.write(answer)

    st.write("### Source Pages")

    st.write(pages)


# In[ ]:




