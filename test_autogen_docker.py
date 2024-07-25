import os
import autogen
import tempfile
import pprint
from autogen import AssistantAgent, UserProxyAgent
from IPython.display import Image, display

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

image_name = "stocks.png"

llm_config = {"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}

chat_result = None

with autogen.coding.DockerCommandLineCodeExecutor(work_dir=temp_dir.name) as code_executor:
    assistant = AssistantAgent("assistant", llm_config=llm_config)
    user_proxy = UserProxyAgent(
        "user_proxy", code_execution_config={"executor": code_executor}
    )

    # Start the chat
    chat_result = user_proxy.initiate_chat(
        assistant,
        # message="Write Python code to calculate the 14th Fibonacci number.",
        message="Plot a chart of NVDA and TESLA stock price change YTD. "
                f"Save the plot to a file called {image_name}.",
    )

print("Before cleanup")
print(temp_dir)
print(os.listdir(temp_dir.name))

# Display the image before cleanup
display_image_path = os.path.join(temp_dir.name, image_name)
print("display_image_path:", display_image_path)
display(Image(display_image_path))

# Clean up the temporary directory after displaying the image
temp_dir.cleanup()
code_executor.stop()  # Stop the docker command line code executor.

# Get the cost of the chat.
pprint.pprint(chat_result.cost)