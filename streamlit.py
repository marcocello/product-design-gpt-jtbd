import os
import importlib
from dotenv import load_dotenv
import pandas as pd
import streamlit as st  
import json
import lib.persona_prompt_generator
import lib.jtbd

load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



def main():

    st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

    st.session_state['step'] = None


    st.subheader('🚀 Gideon: supercharging product design')
    st.markdown("Our platform, Gideon, crafts detailed synthetic Users, conducts insightful job-based interviews, and maps out innovation avenues, all autonomously. Full article [here](https://bootcamp.uxdesign.cc/supercharging-product-design-unleashing-gpt-and-jobs-to-be-done-for-limitless-innovation-ff32fcb2c5a4).")

    openai_api_key = st.text_input(label='Insert your OpenAI API Key')
    
    st.markdown('##### Synthetic Users')
    col1, col2 = st.columns(2)
    with col1:
        profession = st.text_input('Profession of users')
    with col2:
        number = st.number_input('Number of users', min_value=1, max_value=10)


    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        generate_users = st.button('Generate Users')
    with col2:
        delete_users = st.button('Delete Users')

    if delete_users:
        if st.session_state.get('Users'):
            st.session_state['Users'] = None
            st.success('Users deleted!')
        else:
            st.warning('No users to delete')
    if generate_users:
        if profession:
            if openai_api_key:
                with st.spinner(text="Creating users..."):
                    users = lib.persona_prompt_generator.get(number=number, profession=profession, openai_api_key=openai_api_key)
                st.session_state['Users'] = users
            else:
                st.warning('Insert your OpenAI API Key')
        else:
            st.warning('Input the profession')


    if st.session_state.get('Users'):
        users = st.session_state.get('Users')
        data = json.loads(users)
        df = pd.DataFrame(data['personas'])
        st.success('Users generated!')
        edited_df = st.data_editor(df)

    st.markdown('')    
    st.markdown('##### Jobs Map')

    if st.button('Create Jobs Map'):
        if st.session_state.get('Users'):
            if openai_api_key:
                with st.spinner(text="Interviewing users..."):
                    answers = lib.jtbd.get_interviews(personas=st.session_state['Users'], openai_api_key=openai_api_key)
                st.session_state['Answers'] = answers
                st.success('Users interviewed!')
                with st.spinner(text="Creating Jobs Map..."):
                    jobs_map = lib.jtbd.get_jobsmap(answers=answers, openai_api_key=openai_api_key)
                st.session_state['JobsMap'] = jobs_map
                st.success('Jobs Map Created')
            else:
                st.warning('Insert your OpenAI API Key')
        else:
            st.warning("Users not generated")

    if st.session_state.get('JobsMap'):
        jobs_map = st.session_state.get('JobsMap')

        st.text(jobs_map)

if __name__ == "__main__":
    main()
