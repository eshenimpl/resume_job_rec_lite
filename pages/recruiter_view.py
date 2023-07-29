import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import classifier
import matcher

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(2)
        {
            margin-left: auto;
        } 
    </style>
    """,unsafe_allow_html=True
)


with st.container():
    left_col, right_col = st.columns((8,2))
    with left_col:
        st.title("Resume Recommend")
    with right_col:
        if st.button("Switch to job seeker's view"):
            switch_page("candidate_view")

with st.container():
    text_query = st.text_area("Enter your job description here:")   
    if st.button('Recommend'):
        if not text_query:
            st.write('Input Empty. Please enter your job description again.')
        else:
            with st.container():
                st.write('---')
                labels = classifier.predict_subcategory(text_query)
                st.subheader("Tech resume categories you may be interested in:")
                button_container = st.empty()
                button_container.markdown('<div style="white-space: wrap;">' + "".join(
                    [
                        f'<div style="display: inline-block; margin-right: 10px; margin-bottom: 10px; padding: 6px; border: 1px solid #ccc; border-radius: 5px; cursor: pointer">{value}</div>'
                        for value in labels
                    ]
                ) + "</div>", unsafe_allow_html=True,
                )

            with st.container():
                st.write('---')
                recommendation = matcher.recommend_resume(text_query)
                st.subheader("Resume recommendations for you:")
                st.write(recommendation)
                # st.table(recommendation)
