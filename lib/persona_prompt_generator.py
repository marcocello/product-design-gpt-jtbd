from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.memory import ChatMessageHistory
import uuid
import json

def get(number, profession, openai_api_key):
    
    chat = ChatOpenAI(temperature=1, openai_api_key=openai_api_key)

    uuid_number = str(uuid.uuid4())

    prompt = f"""
    Create {number} persona(s)
    Do not generate more than {number} personas
        - each of them that is a {profession} in a different industry
        - has a different experience level
        - put a description about each of them
        - output as json format with the following fields:
            - name
            - profession
            - industry
            - experience_level
            - description


    The output expect is a single json file with the following example:
        {{
            "personas": [
                {{"name": "TBC",

                    "profession": "TBC",
                    "industry": "TBC",
                    "experience_level": "TBC",
                    "description": "TBC"
                }}
            ]
            "control": {uuid_number}
        }}
    """
    
    history = ChatMessageHistory()
    history.add_user_message(prompt)
    ai_response = chat(history.messages)
    output = ai_response.content

    while uuid_number not in ai_response.content:
        history.add_ai_message(ai_response.content)
        ai_response = chat(history.messages)
        output += ai_response.content

    return json.loads(output)