from dotenv import load_dotenv
import streamlit as st  
import lib.jobs
import os
import yaml
import subprocess
import pandas as pd
import math
import lib.persona_prompt_generator
import lib.jtbd



def set_page(name):
    st.set_page_config(page_title=name, page_icon=None, initial_sidebar_state="collapsed")
    st.subheader(name)
    st.markdown("Discover user desires, shape product solutions, and drive innovation with our AI-powered tool that leverages the Jobs-to-be-Done framework and Copilot guidance. \
                Full article [here](https://bootcamp.uxdesign.cc/supercharging-product-design-unleashing-gpt-and-jobs-to-be-done-for-limitless-innovation-ff32fcb2c5a4)")
    st.markdown(f'''Version: {get_git_tag()}''')

def get_git_tag():
    try:
        tag = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip().decode('utf-8')
    except:
        tag = "0.0.0"
    return tag


def main():

    set_page(name="🚀 Gideon: User-Centric Products with AI Copilot")

    default_state = {
        "_openai_api_key":               "",
        "main_jobs_additional_prompt":   "",
        "job_performers_system_prompt": "kdkdkfkmfk",
        "_topic":                       "",
        "_skillset":                    "",
        "_jobs":                        pd.DataFrame(data=None, columns=["Job Performers","Aspiration Job","Big Job","Little Job"]),
        "selected_job_performers":      "",
        "selected_main_job":            "",
        "generated_job_performers":     pd.DataFrame(data=None, columns=["name", "profession", "industry", "experience_level"]),
    }

    state = st.session_state
    for item in default_state:
        if item not in state:
            state[item] = default_state[item]


    tab1, tab2, tab3= st.tabs([
        "Step 1. Discover Job Performers and Main Jobs", 
        "Step 2. Generate Job Performers", 
        "Step 3. Interview Job Performers", 
        # "Step 4. Discover Jobs Map", 
        # "Step 5. Discover Outcomes"
        ])

    
    with st.sidebar:
        settings = dict()
        openai_api_key = st.text_input(label='OpenAI API Key', value=state._openai_api_key, placeholder="sk-XXX")


    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            topic = st.text_area("Topics you are interested and you seek to innovate")
        with col2:    
            skillset = st.text_area("Your skillset")

        with st.expander("Additional prompt", expanded=False):
            state.main_jobs_additional_prompt = st.text_area("Additional prompt", value=state.main_jobs_additional_prompt, label_visibility="collapsed", placeholder="focus on a specific job performers; focus on a specific market, ...")

        
        generate_main_jobs = st.button("Generate", type="primary")
        if generate_main_jobs:
            if openai_api_key:
                if topic:
                    with st.spinner(text=f"Generating Main Jobs and Job Performers..."):
                        jobs = lib.jobs.get(
                            topic=topic,
                            skillset=skillset,
                            jobs=state._jobs,
                            additional_prompt=state.main_jobs_additional_prompt,
                            openai_api_key=openai_api_key)
                        state._jobs = jobs
                        st.rerun()
                else:
                    st.warning('Insert the topic')
            else:
                st.warning("Insert OpenAI API Key in the sidebar")

        
        jobs = st.dataframe(state._jobs, 
                              use_container_width=True, 
                              hide_index=True,
                              )        
            
        col5, col6 = st.columns(2)
        with col5:
            selected_job_performers = st.text_input("Selected Job Performers")
        with col6:
            selected_main_job = st.text_input("Selected Main Job")
        
        selected = st.button("Apply and move to the next section", type="primary")

        if selected:
            state["selected_job_performers"] = selected_job_performers
            state["selected_main_job"] = selected_main_job
            st.rerun()        

    with tab2:

        col1, col2 = st.columns(2)
        with col1:
            profession = st.text_input('Job Performers', value=state["selected_job_performers"])
        with col2:
            number = st.number_input('Number', min_value=1, max_value=10)

        generate_job_performers = st.button('Generate', type="primary", key="generate_job_performers")

        if generate_job_performers:
            if openai_api_key:
                if profession:
                    total_time = 0.5752688172043015*number+15.15591397849463
                    with st.spinner(text=f"Creating users, it should take less than {math.ceil(total_time / 5) * 5} seconds ..."):
                        generated_job_performers = lib.persona_prompt_generator.getV2(number=number, profession=profession, openai_api_key=openai_api_key)
                    st.session_state['generated_job_performers'] = generated_job_performers
                    st.rerun()
                else:
                    st.warning('Input the Job Performers')
            else:
                st.warning("Insert OpenAI API Key in the sidebar")


        generated_job_performers = st.data_editor(state.generated_job_performers, 
                        use_container_width=True, 
                        num_rows= "dynamic", 
                        hide_index=True,
                        )

        selected = st.button("Apply and move to the next section", key="jjr", type="primary")

    with tab3:

        st.markdown("Generated Job performers")
        generated_job_performers = st.dataframe(state.generated_job_performers)
        st.markdown("Selected Main Job")
        selected_main_job = st.text_input("Selected Main Job", key="selected_main_job", value=state.selected_main_job, label_visibility="collapsed")

        interviews = []

        use_main_job_in_interviews = st.toggle('Use the Selected Main Job as interview guideline')
        generate_interview = st.button("Interview", type="primary")

        if generate_interview:
            if openai_api_key:
                for job_performer in state.generated_job_performers.to_dict('records'):
                    print (job_performer)
                    with st.spinner(text=f"""
                                    Interviewing job performers, it should take less than 90 seconds each.\n
                                    Now interviewing {job_performer['name']} ..."""):
                        interviews.append(
                            lib.jtbd.get_single_interview(
                                persona=job_performer, 
                                openai_api_key=openai_api_key, 
                                main_job = state.selected_main_job, 
                                use_main_job = use_main_job_in_interviews)
                        )
                st.session_state['Interviews'] = interviews
                st.success('Users interviewed')
            else:
                st.warning("Insert OpenAI API Key in the sidebar")
                
        if st.button("Show interviews"):


            data = st.session_state['Interviews']
            # Create an empty dictionary to store the data
            data_dict = {}

            # Iterate over the list of dictionaries
            for entry in data:
                name = entry["name"]
                answers = entry["answers"]
                for answer in answers:
                    question = answer["question"]
                    response = answer["answer"]
                    if question not in data_dict:
                        data_dict[question] = {}
                    data_dict[question][name] = response

            # Convert the dictionary to a pandas DataFrame
            df = pd.DataFrame(data_dict)

            # Transpose the DataFrame to match your desired format
            df = df.transpose()

            st.dataframe(df)
        
if __name__ == "__main__":
    main()
