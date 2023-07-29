import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def main():
    st.set_page_config(initial_sidebar_state="collapsed")
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

    st.title("Welcome to the Resume/Job matcher")
    if st.button("I'm a job seeker!"):
        switch_page("candidate_view")
    if st.button("I'm a recruiter!"):
        switch_page("recruiter_view")


if __name__ == '__main__':
    main()
