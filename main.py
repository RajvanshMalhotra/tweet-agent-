from dotenv import load_dotenv
from typing import List,Sequence
load_dotenv()
import os
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END,MessageGraph
# end contains the key for the langgrpahs default ending node, langgraph stops execution when this key is recieved
# message graph: sequence  iof msgs, list of msgs,ouput will be one msg or a couple of msgs
from chains import generation_chain, reflection_chain,process_reflection,process_tweet_feedback

REFLECT="reflect"
GENERATE="generate"

def generate_node(state:Sequence[BaseMessage]):
    # reecives the state which is a sequnece or list of msgs
    return generation_chain.invoke({"messages":state})


def refelection_node(messages:Sequence[BaseMessage])-> List[BaseMessage]:   # the arrow mean what type of data the function will return
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
# print(graph.get_graph())/
# print(graph.get_graph().print_ascii())
# graph.get_graph().print_ascii()






if __name__=='__main__':
    # aagar hum yeh file diorectly chalaye to tabhi niche wala code chalega, this is test code agar yeh file 
    # file import hoti tho iska name== that other file ka name hota to niche wala code nhi chalta, its basically
    # boiler plate code
    # print("hello langgraph")
    print("Testing LangGraph...")
    inputs = HumanMessage(content="""Make this tweet better.
        - This new movie Pushpa 2 was not like the original one. It was trying to impersonate the general scenario set by the industry of extreme riches and showcasing PDA at every step.
    """)

    try:
        print("Invoking graph with input...")
        results = graph.invoke(inputs)
        for result in results:
            parsed_output = result.content  # Assuming result.content is a string
            print(f"Output: {parsed_output}")
        # print("Results:", results)
    except Exception as e:
        print(f"Error during graph invocation: {e}")
