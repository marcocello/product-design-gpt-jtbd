from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import json
import uuid

def get_single_interview(persona, openai_api_key, main_job, use_main_job):

  additional_prompt = ""
  if use_main_job:
    additional_prompt = f"""
    Answer the following question focusing and thinking about the main job \"{main_job}\" applied to what you are doing as {persona["profession"]}
    If the main job \"{main_job}\" is not related to you, simply answer \"This is not my main job\" and skip the question.
    """

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

  uuid_number = str(uuid.uuid4()) 
  
  prompt = f"""
  Interview this job performer:
  {json.dumps(persona)}

  {additional_prompt}

  This is the list of questions:
  {questions}

  The output expect is a json file with the following example:
        {{
            "name": "{persona['name']}",
            "answers": [
                {{
                  "question": "",
                  "answer": ""
                }}
              ]
            "control": {uuid_number}
        }}    
  """
  print (prompt)

  chat = ChatOpenAI(openai_api_key=openai_api_key)

  history = ChatMessageHistory()
  history.add_user_message(prompt)
  ai_response = chat(history.messages)
  output = ai_response.content

  while uuid_number not in ai_response.content:
      history.add_ai_message(ai_response.content)
      ai_response = chat(history.messages)
      output += ai_response.content

  return json.loads(output)


  # history = ChatMessageHistory()
  # history.add_user_message(prompt)
  # import time
  # start_time = time.time()
  # ai_response = chat(history.messages)
  # print("--- %s seconds ---" % (time.time() - start_time))
  # print(ai_response.content)
  # return json.loads(ai_response.content)



def summarize_answers(question, answers, openai_api_key):

  uuid_number = str(uuid.uuid4()) 
  prompt = f"""
  This is the question
  {json.dumps(question)}

  And those are the answers from the personas generated
  {json.dumps(answers)}

  Please summarize the answers and create a summarized_answer.

  The output expect is a json file with the following example:
        {{
            "summarized_answer": {{
              "question": "",
              "summarized_answer": ""
            }}
            "control": {uuid_number}
        }}    
  """

  chat = ChatOpenAI(openai_api_key=openai_api_key)

  history = ChatMessageHistory()
  history.add_user_message(prompt)
  ai_response = chat(history.messages)
  output = ai_response.content

  while uuid_number not in ai_response.content:
      history.add_ai_message(ai_response.content)
      ai_response = chat(history.messages)
      output += ai_response.content

  return json.loads(output)


  # history = ChatMessageHistory()
  # history.add_user_message(prompt)
  # import time
  # start_time = time.time()
  # ai_response = chat(history.messages)
  # print("--- %s seconds ---" % (time.time() - start_time))
  # print(ai_response.content)
  # return json.loads(ai_response.content)



def get_interviews(personas, openai_api_key):
  answers = dict()

  for persona in personas['personas']:
    interview = get_single_interview(persona, openai_api_key)
    answers[persona['name']] = json.loads(interview)

  return answers

def get_jobsmap(personas, answers, openai_api_key):

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
            HumanMessage(content=f"""Those are the personas {json.dumps(personas)} and those are the questions and answers from those personas {json.dumps(answers)}"""),
        ]
    )
    return json.loads(jobs_map.content)

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


def main():
  import persona_prompt_generator
  import os
  from dotenv import load_dotenv

  load_dotenv()

  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  personas = persona_prompt_generator.get(number=2, profession="UX Designer", openai_api_key=OPENAI_API_KEY)

  answers = dict()
  for persona in personas['personas']:
    print(persona['name'])
    answers[persona['name']] = get_single_interview(persona=persona, openai_api_key=OPENAI_API_KEY)
          
  
  jobs_map = get_jobsmap(answers,openai_api_key=OPENAI_API_KEY)
 
  with open("answers.json", 'w') as file:
    json.dump(answers, file)


if __name__ == "__main__":
  main()