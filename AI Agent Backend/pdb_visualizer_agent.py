# pdb_visualizer_agent.py

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
import os
import py3Dmol

# -----------------------------
# Define the visualizer function
# -----------------------------
def visualize_pdb(pdb_id: str) -> str:
    pdb_id = pdb_id.strip().lower()
    pdb_file = f"./downloads/{pdb_id}.pdb"

    if not os.path.exists(pdb_file):
        return f"PDB file {pdb_file} not found. Please download it first."

    with open(pdb_file, "r") as f:
        pdb_data = f.read()

    view = py3Dmol.view(width=400, height=300)
    view.addModel(pdb_data, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    html = view._make_html()

    html_path = f"./downloads/{pdb_id}.html"
    with open(html_path, "w") as f:
        f.write(html)

    return f"Visualization of {pdb_id.upper()} saved to {html_path}"

# -----------------------------
# Wrap it in a tool
# -----------------------------
pdb_visualizer_tool = Tool(
    name="PDBVisualizerTool",
    func=visualize_pdb,
    description="Generates an HTML visualization of a PDB ID. Input: 4-character PDB ID (e.g., 1jd4)."
)

# -----------------------------
# Create the agent
# -----------------------------
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    openai_api_key="sk"
)

pdb_visualizer_agent = initialize_agent(
    tools=[pdb_visualizer_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
