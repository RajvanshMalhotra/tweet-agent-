from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI 
# from groq.api import onnx
from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
# from langchain_core.output_parsers import JsonOutputParser

# parser = JsonOutputParser(pydantic_object={
#     "type": "object",
#     "properties": {
#         "name": {"type": "string"},
#         "price": {"type": "number"},
#         "features": {
#             "type": "array",
#             "items": {"type": "string"}
#         }
#     }
# })
# parser=JsonOutputParser()
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

# model=ChatOpenAI()
# model=ChatGoogleGenerativeAI(model="gemini-1.5-pro")
model=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

generation_chain=generation_prompt | model
reflection_chain= reflection_prompt | model

parser = StrOutputParser()

# # Function to process tweet feedback and return string output
# def process_tweet_feedback(input_messages):
#     # Run the generation chain with input messages
#     generated_output = generation_chain.run(input_messages)
    
#     # Parse the output using StrOutputParser
#     parsed_output = parser.parse(generated_output)
    
#     return parsed_output  # This will be a string output

# def process_reflection(input_messages):
#     # Run the reflection chain with input messages
#     reflection_output = reflection_chain.run(input_messages)
    
#     # Parse the output using StrOutputParser
#     parsed_output = parser.parse(reflection_output)
    
#     return parsed_output  # This will be a string output

