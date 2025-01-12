from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
reflection_prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a viral twitter influencer grading a tweet. Generate critique and recommendations for the users tweet, always provide detailed recommendations,including requests for length, virality,style,etc",

        ),
        MessagesPlaceholder(variable_name="messages"),


    ]
)

generation_prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a twitter influencer assistant tasked with writing excellent twitter posts."
            "generate the best twitter post possible for the user's requests."
            "if the userprovides critique, respond with a revised version of your  previious attempts. ",

        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


model=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

generation_chain=generation_prompt | model
reflection_chain= reflection_prompt | model

parser = StrOutputParser()

#     return parsed_output  # This will be a string output

