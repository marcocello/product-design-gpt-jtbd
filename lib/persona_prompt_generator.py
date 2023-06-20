from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def get(number, profession, openai_api_key):
    
    chat = ChatOpenAI(temperature=1, openai_api_key=openai_api_key)

    prompt = f"""
    Create {number} persona(s)
        - each of them that is a {profession} in a different industry
        - has a different experience level
        - put a description about each of them
        - output as json format with the following fields:
            - name
            - profession
            - industry
            - experience_level
            - description
    Do not generate more than {number} personas

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
        }}
    """

    return chat([HumanMessage(content=prompt)]).content