import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import classifier
import matcher
import totext


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
        st.title("Job Recommend")
    with right_col:
        if st.button("Switch to recruiter's view"):
            switch_page("recruiter_view")

with st.container():
    left_col, right_col = st.columns((4,6))
    with left_col:
        input_method = st.selectbox("Select Input Method", ["Text", "Upload PDF"])
    with right_col:
        if input_method == "Text":
            text_query = st.text_area("Enter your resume here:")
        elif input_method == "Upload PDF":
            uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
            if uploaded_file is not None:
                text_query = totext.extract_from_pdf(uploaded_file)

    if st.button('Recommend'):
        if not text_query:
            st.write('Input Empty. Please input your resume again.')
        else:
            with st.container():
                st.write('---')
                labels = classifier.predict_subcategory(text_query)
                st.subheader("Tech job categories you may be interested in:")
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
                recommendation = matcher.recommend_job(text_query)
                st.subheader("Job recommendations for you:")
                st.write(recommendation)
                # st.table(recommendation)