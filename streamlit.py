import os
import importlib
from dotenv import load_dotenv
import pandas as pd
import streamlit as st  
import json
import lib.persona_prompt_generator
import lib.jtbd

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



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
                    users = lib.persona_prompt_generator.get(number=number, profession=profession, openai_api_key=OPENAI_API_KEY)
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
                    answers = lib.jtbd.get_interviews(personas=st.session_state['Users'], openai_api_key=OPENAI_API_KEY)
                st.session_state['Answers'] = answers
                st.success('Users interviewed!')
                with st.spinner(text="Creating Jobs Map..."):
                    jobs_map = lib.jtbd.get_jobsmap(answers=answers, openai_api_key=OPENAI_API_KEY)
                st.session_state['JobsMap'] = jobs_map
                st.success('Jobs Map Created')
            else:
                st.warning('Insert your OpenAI API Key')
        else:
            st.warning("Users not generated")

    if st.session_state.get('JobsMap'):
        jobs_map = st.session_state.get('JobsMap')

        st.text(jobs_map)

    # if answers:
    #     # Jobs map

    #     col1.subheader('Generate Jobs Map')
    #     if col1.button('Generate Jobs Map'):
    #         jobs_map = lib.jtbd.get_jobsmap(answers=answers, openai_api_key=OPENAI_API_KEY)
    #         with col2:
    #             col2.subheader('Jobs Map')
    #             col2.write(jobs_map)

    # if jobs_map:
    # # Outcomes
    #     with col1:
    #         col1.subheader('Generate Outcomes')
    #         if col1.button('Generate Outcomes'):
    #             outcomes = lib.jtbd.get_outcomes(answers=answers, jobs_map=jobs_map, openai_api_key=OPENAI_API_KEY)
    #             with col2:
    #                 col2.subheader('Outcomes')
    #                 col2.write(outcomes)

    # with col2:

    # with st.sidebar:

    #     # st.markdown("Progress")
    #     # if st.session_state['step'] == "Step1":
    #     #     st.success('✅ Generate Users')
    #     # else:
    #     #     st.info('Generate Users')

    #     # if st.session_state['step'] == "Generate Interviews":
    #     #     st.success('Generate Interviews')
    #     # else:
    #     #     st.info('Step2')

    #     # if st.session_state['step'] == "Step3":
    #     #     st.success('Step3')
    #     # else:
    #     #     st.info('Step3')

    #     # st.divider()
    #     openai_api_key = st.text_input(label='ooo', label_visibility='hidden',placeholder='OpenAI API Key')


if __name__ == "__main__":
    main()

# import streamlit as st
# from streamlit_option_menu import option_menu



# # 1. as sidebar menu


#     # selected = option_menu("Status", ["Generate Syntetic Users", 'Generate Interviews'], 
#     #     icons=['gear', 'gear'], menu_icon="cast", default_index=1)
#     # selected

# # 2. horizontal menu
# def on_change(key):
#     selection = st.session_state[key]
#     st.write(f"Selection changed to {selection}")

# selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     menu_icon="cast", default_index=0, orientation="horizontal",
#     styles={
#         "container": {"padding": "0!important", "background-color": "#fafafa"},
#     })

# with st.sidebar:
#     openai_api_key = st.text_input('OpenAI API Key')

# st.title('Gideon')
# st.subheader('Supercharging Product Design: Unleashing GPT and Jobs-to-be-Done for Limitless Innovation')



# st.session_state['step'] = None

# col1, col2 = st.columns([3,1])
# with col1:
#     step1 = st.button("Move to Step 1")
#     step2 = st.button("Move to Step 2")
#     step3 = st.button("Move to Step 3")

#     if step1:
#         st.session_state['step'] = "Step1"

#     if step2:
#         st.session_state['step'] = "Step2"

#     if step3:
#         st.session_state['step'] = "Step3"


# with col2:

#     st.text("Activity Progress")
#     if st.session_state['step'] == "Step1":
#         st.success('Step1')
#     else:
#         st.info('Step1')

#     if st.session_state['step'] == "Step2":
#         st.success('Step2')
#     else:
#         st.info('Step2')

#     if st.session_state['step'] == "Step3":
#         st.success('Step3')
#     else:
#         st.info('Step3')
