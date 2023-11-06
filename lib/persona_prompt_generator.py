import uuid
import json
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory

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


def getV2(number, profession, openai_api_key):

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        """
        You are an advacend AI able to syntetic generate personas very detailed, precised and realistic.
        """),
        ("human", """
        
        Create only a specific {number} persona(s).
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
            """)
    ])

    functions = [
        {
        "name": "json",
        "description": "create the json",
        "parameters": {
            "type": "object",
            "properties": {
                "aaa": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "item": {
                            "name": {"type": "string"},
                                "profession": {"type": "string"},
                                "industry": {"type": "string"},
                                "experience_level": {"type": "string"},
                                "description": {"type": "string"},
                                }
                            }
                        },
                },
                "required": ["aaa"]
            },
        },
    ]

    rag_chain = (
        prompt 
        | llm.bind(function_call={"name": "json"}, functions = functions)
    )

    res = rag_chain.invoke({"number": number, "profession": profession})

    input_string = res.additional_kwargs['function_call']['arguments']

    import json 

    
    cleaned_string = input_string.replace('\n', '')

    parsed_json = json.loads(cleaned_string)

    return pd.DataFrame(parsed_json["personas"])

