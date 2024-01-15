import os
from crewai import Agent, Task, Crew, Process

#os.environ["OPENAI_API_KEY"] = "YOUR KEY"
# You can choose to use a local model through Ollama for example.
#
from langchain.llms import Ollama
ollama_llm = Ollama(model="mistral", temperature=0)

# Install duckduckgo-search, wikipedia for this example:
# !pip install -U duckduckgo-search
# !pip install --upgrade --quiet  wikipedia

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
concept_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

topic = 'Network Vulnerability Scan'
# Define your agents with roles and goals
researcher = Agent(
  role='Internet Research Analyst',
  goal=f'Define the steps of a process to execute a {topic}',
  backstory=f"""You work at an information security provider.
  Your expertise lies in identifying all the detailed steps and procedures to complete a {topic}""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
    llm=ollama_llm # was defined above in the file
)

definer = Agent(
  role='Internet Research Analyst #2',
  goal=f'Generate a clear definition of concepts {topic}',
  backstory=f"""You work at an information security provider.
  Your expertise lies in identifying all relevant concepts related with a {topic}""",
  verbose=True,
  allow_delegation=False,
  tools=[concept_tool],
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
    llm=ollama_llm # was defined above in the file
)


writer = Agent(
  role='Security Product Manager',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a Product Manager for cybersecurity products, known for
  your insightful and engaging communication.
  You review the given content and ensure that complex concepts are clearly exposed.""",
  verbose=True,
  allow_delegation=False,
  llm=ollama_llm
)

# Create tasks for your agents
task1 = Task(
  description=f"""Define what is a {topic}.
  Identify all relevant concepts related with a {topic}
  Your final answer MUST contain all the main concepts related with a {topic} """,
  agent=definer
)

task2 = Task(
  description=f"""Conduct a comprehensive analysis of the steps to perform a {topic}.
  Identify all operational actions, and the input and output of each step of the process.
  Your final answer MUST list all sequential tasks and subtasks required to perform a {topic}""",
  agent=researcher
)
task3 = Task(
  description=f"""Based on the previous output, create a mermaid diagram of all the tasks required to perform a {topic}.""",
  agent=writer
)
task4 = Task(
  description=f"""Using the insights provided, review and improve if required the text, to ensure that the output is  
  informative to a technical and executive audience.
  Your final answer MUST include the advantages and disadvantages of performing a {topic} in two paragraphs.""",
  agent=writer
)



# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, definer, writer],
  tasks=[task1, task2, task3, task4],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)