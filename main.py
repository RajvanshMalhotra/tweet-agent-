from dotenv import load_dotenv
from typing import List,Sequence
load_dotenv()
import os
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END,MessageGraph
from chains import generation_chain, reflection_chain,process_reflection,process_tweet_feedback

REFLECT="reflect"
GENERATE="generate"

def generate_node(state:Sequence[BaseMessage]):
    return generation_chain.invoke({"messages":state})


def refelection_node(messages:Sequence[BaseMessage])-> List[BaseMessage]:   
    res=reflection_chain.invoke({"messages":messages})
    return [HumanMessage(content=res.content)]

builder=MessageGraph()
builder.add_node(GENERATE,generate_node)
builder.add_node(REFLECT,refelection_node)
builder.set_entry_point(GENERATE)
 
def should_continue(state: List[BaseMessage]):
    if(len(state)>6):
        return END
    return REFLECT
builder.add_conditional_edges(GENERATE,should_continue)
builder.add_edge(REFLECT,GENERATE)
graph=builder.compile()

if __name__=='__main__':
    print("Testing LangGraph...")
    inputs = HumanMessage(content="""Make this tweet better.
        - This new movie Pushpa 2 was not like the original one. It was trying to impersonate the general scenario set by the industry of extreme riches and showcasing PDA at every step.
    """)

    try:
        print("Invoking graph with input...")
        results = graph.invoke(inputs)
        for result in results:
            parsed_output = result.content  
            print(f"Output: {parsed_output}")
    except Exception as e:
        print(f"Error during graph invocation: {e}")
