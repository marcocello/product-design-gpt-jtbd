import os
import importlib
from dotenv import load_dotenv
import pandas as pd
import streamlit as st  
import json
import lib.persona_prompt_generator
import lib.jtbd
import math

load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import subprocess

def get_git_tag():
    try:
        tag = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip().decode('utf-8')
    except:
        tag = "Unknown"
    return tag

def main():

    st.set_page_config(page_title="🚀 Gideon - Supercharging Product Design", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

    st.session_state['step'] = None


    st.subheader('🚀 Gideon - Supercharging Product Design')
    st.markdown("Our platform, Gideon, crafts detailed synthetic Users, conducts insightful job-based interviews, and maps out innovation avenues, all autonomously. Full article [here](https://bootcamp.uxdesign.cc/supercharging-product-design-unleashing-gpt-and-jobs-to-be-done-for-limitless-innovation-ff32fcb2c5a4).")

    st.markdown(f"Version: {get_git_tag()}")
    openai_api_key = st.text_input(label='Insert your OpenAI API Key')
    
    st.markdown('##### Users')
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
                total_time = 0.5752688172043015*number+15.15591397849463
                with st.spinner(text=f"Creating users, it should take less than {math.ceil(total_time / 5) * 5} seconds ..."):
                    users = lib.persona_prompt_generator.get(number=number, profession=profession, openai_api_key=openai_api_key)
                st.session_state['Users'] = users
            else:
                st.warning('Insert your OpenAI API Key')
        else:
            st.warning('Input the profession')


    if st.session_state.get('Users'):
        users = st.session_state.get('Users')
        df = pd.DataFrame(users['personas'])
        st.success('Users generated')
        edited_df = st.data_editor(df)

    st.markdown('')    
    st.markdown('##### Jobs Map')

    if st.button('Create Jobs Map'):
        if st.session_state.get('Users'):
            if openai_api_key:
                answers = dict()
                users = st.session_state.get('Users')
                for persona in users['personas']:

                    with st.spinner(text=f"""
                                    Interviewing users, it should take less than 90 seconds each.\n
                                    Now interviewing user \"{persona['name']}\" ..."""):
                        answers[persona['name']] = lib.jtbd.get_single_interview(persona=persona, openai_api_key=openai_api_key)
                st.session_state['Answers'] = answers
                st.success('Users interviewed')

                answers = st.session_state['Answers']
                new_answers = {}

                for user, qa_list in answers.items():
                    for qa in qa_list['answers']['answers']:
                        question = qa["question"]
                        
                        if question not in new_answers:
                            new_answers[question] = []

                        new_answers[question].append({"user": user, "answer": qa["answer"]})

                with st.spinner(text="Summarizing interviews, it should take less than 200 seconds ..."):
                    summarized_answers = dict()
                    for question in new_answers:
                        res = lib.jtbd.summarize_answers(question=question,answers=new_answers[question],openai_api_key=openai_api_key)
                        summarized_answers[question] = res["summarized_answer"]
                st.success('Interviews summarized')

                with st.spinner(text="Creating Jobs Map, it should take less than 20 seconds ..."):
                    jobs_map = lib.jtbd.get_jobsmap(personas=users['personas'], answers=summarized_answers, openai_api_key=openai_api_key)
                st.session_state['JobsMap'] = jobs_map
                st.success('Jobs Map Created')
            else:
                st.warning('Insert your OpenAI API Key')
        else:
            st.warning("Users not generated")

    if st.session_state.get('JobsMap'):
        jobs_map = st.session_state.get('JobsMap')
        col1, col2 = st.columns([3,1])
        with col1:
            st.json(json.dumps(jobs_map))
        with col2:
            st.download_button('Download', json.dumps(jobs_map), file_name=f'JobsMap-{jobs_map["Main Job"].replace(" ", "")}.txt',)

if __name__ == "__main__":
    main()
