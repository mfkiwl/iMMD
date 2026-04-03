# main_agent.py

import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from pdb_download_agent import pdb_download_agent
from pdb_visualizer_agent import pdb_visualizer_agent
from file_checker_agent import file_checker_agent
from multiscale_simulation_agent import multiscale_simulation_agent


llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    openai_api_key="sk"
)

file_checker_router_tool = Tool(
    name="FileCheckerAgent",
    func=file_checker_agent.run, 
    description="Delegates file existence checks to a file checker agent. Input: full file path."
)

pdb_download_router_tool = Tool(
    name="PDBDownloadAgent",
    func=pdb_download_agent.run,
    description="Delegates PDB downloads to the PDBDownloadAgent. Input: PDB ID.",
    return_direct=True
)

pdb_visualizer_router_tool = Tool(
    name="PDBVisualizerAgent",
    func=pdb_visualizer_agent.run,
    description="Delegates PDB visualization to the PDBVisualizerAgent. Input: 4-character PDB ID.",
    return_direct=True
)

multiscale_router_tool = Tool(
    name="MultiscaleSimulationAgent",
    func=multiscale_simulation_agent.run,
    description="Runs a full multiscale MD simulation loop on a PDB file. Input can be a full sentence like 'simulate 1jd4 for 3 steps on CPU'",
    return_direct=True
)

agent = initialize_agent(
    tools=[file_checker_router_tool, pdb_download_router_tool, pdb_visualizer_router_tool, multiscale_router_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
