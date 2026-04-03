# pdb_download_agent.py

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
import os
import requests

# -----------------------------
# Actual download function
# -----------------------------
def download_pdb_file(pdb_id: str) -> str:
    pdb_id = pdb_id.strip().lower()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            output_path = f"./downloads/{pdb_id}.pdb"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "w") as f:
                f.write(response.text)

            return f"Downloaded PDB {pdb_id.upper()} and saved to {output_path}"
        else:
            return f"Could not download PDB ID {pdb_id.upper()} (HTTP {response.status_code})"

    except Exception as e:
        return f"Error downloading {pdb_id.upper()}: {str(e)}"


# -----------------------------
# Define PDB download tool
# -----------------------------
pdb_download_tool = Tool(
    name="PDBDownloaderTool",
    func=download_pdb_file,
    description="Downloads a PDB file by 4-character ID (e.g. 1jd4)."
)


# -----------------------------
# Create the dedicated agent
# -----------------------------
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    openai_api_key="sk"
)

pdb_download_agent = initialize_agent(
    tools=[pdb_download_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
