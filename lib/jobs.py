
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

def get(topic, skillset, jobs, additional_prompt, openai_api_key):


    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    # vectorstore = Pinecone.from_existing_index(pinecone_index_name, OpenAIEmbeddings())
    # retriever=vectorstore.as_retriever()


    prompt = ChatPromptTemplate.from_messages([
        ("system", """     
        You are a business expert and visionary and an expert and advisor of Jobs-to-be-done. 
        Based on the topic and the skillset you will receive from the user you have to generate a set of different Job Peformers and Main Jobs.

        Those are characteristics of good Jobs, plese use those:

        - Clear and concise phrasing: The main job should be described in a way that is easily understandable and relatable to the target audience. For example, "Find a reliable babysitter" or "Plan a vacation itinerary."
        - One-dimensional focus: The main job should be focused on a single outcome or goal. It should not be overly complex or multifaceted. For example, "Lose weight" or "Find a new job."
        - End state orientation: The main job should have a clear end point or desired outcome. It should be formulated in a way that implies completion or achievement. For example, "Buy a new car" or "Renovate the kitchen."
        - Chronological mapping: The main job can be illustrated as a sequence of stages, with each stage representing a smaller job within the main job. This helps to understand the progression and steps involved in achieving the main job. For example, "Plan a wedding: 1. Set a date, 2. Choose a venue, 3. Select a caterer, 4. Find a dress, 5. Send out invitations."
        - Social and emotional aspects: The main job should consider the social and emotional aspects that are important to the customer. This includes any social or emotional needs or desires that are associated with the main job. For example, "Feel confident in my appearance" or "Create lasting memories with loved ones."
        - Iterative refinement: The definition of the main job should be continuously refined and improved over time. This can be done through feedback from customers and stakeholders, as well as using tools like a thesaurus to find the best labels.

        Those are the difference among Aspiration Jobs, Main Jobs and Little Jobs:
        - Aspiration Jobs: These are ideal changes of state that individuals desire to become. They represent higher-level objectives and are more abstract. Example: Enjoy the freedom of mobility.
        - Main Jobs: These are broader objectives that are typically at the level of a main job. They are more specific than aspiration jobs but still represent a larger goal. Example: Get to a destination on time.
        - Little Jobs: These are smaller, more practical jobs that correspond roughly to stages in a big job. They are more concrete and specific tasks that need to be accomplished to achieve the main job. Example: Park the vehicle.
        
    """),

        ("human", """
        
        Generate 5 objects on {topic}, each of them has:
            - Job Performer
            - Aspiration Job
            - Main Job
            - Little Job

        {additional_prompt}
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
                            "Job_Perfomers": {"type": "string"},
                                "Aspiration_Job": {"type": "string"},
                                "Main_Job": {"type": "string"},
                                "Little_Job": {"type": "string"},
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

    res = rag_chain.invoke({"topic": topic, "skillset": skillset, "additional_prompt": additional_prompt})


    input_string = res.additional_kwargs['function_call']['arguments']

    import json 


    cleaned_string = input_string.replace('\n', '')

    parsed_json = json.loads(cleaned_string)


    
    return pd.DataFrame(parsed_json["objects"])


