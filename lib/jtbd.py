from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import json

def get_interviews(personas, openai_api_key):

    questions = """
    Tell me a little about yourself and what you do.
    When was the last time you did the main job?
    How did you feel overall while getting that job done?

    What are you trying to accomplish? What tasks are involved?
    What problems are you trying to prevent or resolve?
    What helps you achieve your goals?
    What would the ideal service be to do the job for you?”
    What else are you trying to get done?”

    How do you get started?
    What is the previous step? What's the next step?
    How do you continue after that?
    How do you make decisions along the way?
    How do you feel at each stage in the process?
    How do you know you are doing the job right?
    How do you wrap things up?

    What workarounds exist in your process?
    What do you dread doing? What do you avoid? Why?
    What could be easier? Why?
    Why do you avoid doing certain parts of the job?
    What's the most annoying part? Why is that frustrating?
    How do you feel when the job is completed?

    In which situations do you act differently?
    What conditions influence your decisions?
    How do the environment and setting affect your attitude and feelings while getting the job done?
    """

    chat = ChatOpenAI(openai_api_key=openai_api_key)

    prompt = f"""
    Those are the personas
    {personas}

    For each of them, answer the following questions:
    {questions}

    The output expect is a json file with the following example:
        [
            {{"question": "TBC",
                "answers": [{{
                    "persona": "TBC",
                    "answer": "TBC"
                    }}
                ]
        ]
        }}
    """

    return chat([HumanMessage(content=prompt)]).content

def get_jobsmap(answers, openai_api_key):

    chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

    history = ChatMessageHistory()

    jobs_map = chat(
        [
            SystemMessage(content="""
            You are a Jobs-to-be-done expert with multiple years of experience. You are very knowledgeable about the Jobs-to-be-done books
            like The Jobs to be Done Playbook by Jim Kalbach and What Customers Want: Using Outcome-Driven Innovation to Create Breakthrough Products and Services by Anthony Ulwick.
            You have a lot of experience in applying the Jobs-to-be-done framework in practice. You are a very good listener and you are
            able to ask the right questions to get to the core of the problem. You are able to create a jobs map for any job in any industry.

            The user will provide you with a list of questions and answers from users and you need to provide the main job and a jobs map.
            
            The output expect is a json file. Here an example:
            {
                "Main Job": "TBC",
                "Define - Determine objectives and plan how to get the job done.": [
                    {
                        "jobs": "TBC"
                    }],
                "Locate - Gather materials and information needed to do the job.": [
                    {
                        "jobs": "TBC"
                    }],
                "Prepare - Organize materials and create the right setup.": [
                    {
                        "jobs": "TBC"
                    }], 
                "Confirm - Ensure that everything is ready to perform the job.": [
                    {
                        "jobs": "TBC"  
                    }],
                "Execute - Perform the job as planned.": [
                    {
                        "jobs": "TBC"
                    }],
                "Monitor - Evaluate success as the job is executed.": [
                    {
                        "jobs": "TBC"
                    }],
                "Modify - Modify and iterate as necessary.": [
                    {
                        "jobs": "TBC"
                    }], 
                "Conclude - End the job and follow-up.": [
                    {
                        "jobs": "TBC"
                    }]  
            }
            """),
            HumanMessage(content=answers),
        ]
    )


    return jobs_map.content

def get_outcomes(answers, jobs_map, openai_api_key):

    chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

    history = ChatMessageHistory()

    outcomes = chat(
        [
            SystemMessage(content="""
            You are a Jobs-to-be-done expert with multiple years of experience. You are very knowledgeable about the Jobs-to-be-done books
            like The Jobs to be Done Playbook by Jim Kalbach and What Customers Want: Using Outcome-Driven Innovation to Create Breakthrough Products and Services by Anthony Ulwick.
            You have a lot of experience in applying the Jobs-to-be-done framework in practice. You are a very good listener and you are
            able to ask the right questions to get to the core of the problem. You are able to create a jobs map for any job in any industry.

            The user will provide you with a list of questions and answers from users and the jobs map created and you need to provide a list of outcomes (following the Outcome-Driven Innovation framework) for each job

            The output expect is a json file. Here an example:
{
  "Main Job": "TBC",
  "Define - Determine objectives and plan how to get the job done.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Locate - Gather materials and information needed to do the job.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Prepare - Organize materials and create the right setup.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Confirm - Ensure that everything is ready to perform the job.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Execute - Perform the job as planned.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Monitor - Evaluate success as the job is executed.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Modify - Modify and iterate as necessary.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  },
  "Conclude - End the job and follow-up.": {
    "jobs": [
      {
        "job": "TBC"
      }
    ],
    "outcomes": [
      {
        "outcome": "TBC",
        "metrics": "TBC"
      }
    ]
  }
}
            """),
            HumanMessage(content=f"""
            those are the {answers} and the jobs map: {jobs_map}
            """),
        ]
    )


    return outcomes.content
