import os
import yaml
from crewai import Crew, Agent, Task, Process
from dotenv import load_dotenv
load_dotenv()


#screenwriting 

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "../config")  # path to config folder

# Load agents
with open(os.path.join(CONFIG_DIR, "agents.yaml")) as f:
    agents_config = yaml.safe_load(f)

agents = {name: Agent(**cfg) for name, cfg in agents_config.items()}

# Load tasks
with open(os.path.join(CONFIG_DIR, "tasks.yaml")) as f:
    tasks_config = yaml.safe_load(f)

tasks = []
for task in tasks_config.values():
    tasks.append(Task(
        description=task["description"],
        expected_output=task["expected_output"],
        agent=agents[task["agent"]]
    ))

# Create Crew
crew = Crew(
    agents=list(agents.values()),
    tasks=tasks,
    process=Process.sequential,
    verbose=True
)

# Run
result = crew.kickoff(inputs={"movie_concept": "A detective who finds out he is the killer"})
print(result)
