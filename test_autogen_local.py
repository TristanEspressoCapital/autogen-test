import os
import autogen
import tempfile
import pprint
from autogen import AssistantAgent, UserProxyAgent
from IPython.display import Image

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

image_name = "stocks.png"

llm_config = {"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}
assistant = AssistantAgent("assistant", llm_config=llm_config)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir=temp_dir.name)}
)

# Start the chat
chat_result = user_proxy.initiate_chat(
    assistant,
    # message="Write Python code to calculate the 14th Fibonacci number.",
    message="Plot a chart of NVDA and TESLA stock price change YTD. "
            f"Save the plot to a file called {image_name}.",
)

print(os.listdir(temp_dir.name))
Image(os.path.join(temp_dir, image_name))

temp_dir.cleanup()

# Get the cost of the chat.
pprint.pprint(chat_result.cost)