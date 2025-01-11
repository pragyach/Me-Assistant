from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from tools_config import TOOLS

# Initialize OpenAI LLM
llm = OpenAI(temperature=0, model="text-davinci-003", openai_api_key="your_openai_api_key")

# Initialize the agent with tools
agent = initialize_agent(TOOLS, llm, agent="zero-shot-react-description", verbose=True)

# Agent loop
def agent_loop():
    print("Multi-Agent Workflow Initialized")
    print("Type 'exit' to quit.")
    
    while True:
        user_query = input("\nEnter your query: ")
        if user_query.lower() == "exit":
            print("Exiting...")
            break

        # Process user query
        response = agent.run(user_query)
        print("\nAgent Response:")
        print(response)

# Run the workflow
if __name__ == "__main__":
    agent_loop()
