from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize proxy client
proxy_client = get_proxy_client('gen-ai-hub')

# Set up the chat model
chat_llm = ChatOpenAI(proxy_model_name='gpt-35-turbo', proxy_client=proxy_client)

# Define the prompt
prompt_template = PromptTemplate(input_variables=["text"], template="Translate to Danish: {text}")

# Create the LLMChain
chain = LLMChain(llm=chat_llm, prompt=prompt_template)

# Run the chain with the input text
response = chain.run("Guten Morgen")

# Print the output
print(response)
    