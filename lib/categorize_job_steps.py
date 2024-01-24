import json
import os
import pandas as pd

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")
TEMPERATURE = os.getenv("TEMPERATURE")

model = ChatOpenAI(model_name=MODEL, temperature=TEMPERATURE)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
     
        You are a multi-year expert in Jobs-to-be-done expert with very knowledgeable about the Jobs-to-be-done book like The Jobs to be Done Playbook by Jim Kalbach.
     
        You will receive a table as input and you will list the job steps from a job performer. Based on the main job you have to categorize each job step.
     """),
    
    ("human", """


This is the main job "{main_job}" that the job performers "{job_performers}" are trying to achieve. Those are the job steps {job_steps} that we discovered.

Please categorize each job step into one of the following categories:

- Define: Determine objectives and plan how to get the job done.
- Locate: Gather materials and information needed to do the job.
- Prepare: Organize materials and create the right setup.
- Confirm: Ensure that everything is ready to perform the job.
- Execute: Perform the job as planned.
- Monitor: Evaluate success as the job is executed.
- Modify: Modify and iterate as necessary.
- Conclude: End the job and follow-up.

If you are unable to categorize a job step, please use the additional category "uncategorized."

Output format (generate only the JSON file below):


{{
    "Category": "",
    "Job Step": ""
}}

    

""")]
)


chain = (
    prompt 
    | model)