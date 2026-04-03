# multiscale_simulation_agent.py

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
import subprocess
import os
import argparse
import shlex

# You can move this out if needed
def run_step(cmd, label):
    print(f"\n🚀 Running: {label}")
    print(f"🧾 Command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {label}")

def multiscale_loop(n_iter: int, path: str, platform: str, start_pdb: str) -> str:
    print(f"🔁 Starting multiscale loop for {n_iter} iterations in base path: {path}\n")

    for i in range(1, n_iter + 1):
        print(f"\n============================")
        print(f"🔁 ITERATION {i}")
        print(f"============================\n")

        if i == 1:
            aa_input_pdb = os.path.abspath(start_pdb)
        else:
            aa_input_pdb = os.path.join(path, f"AA-MD-{i}", f"AA-MD-{i}-solu-initial.pdb")

        run_step(["python", "Test_AA.py", "--iteration", str(i), "--path", path, "--pdb_file", aa_input_pdb],
                 f"AA-MD iteration {i}")

        run_step(["python", "Test_AA_CG.py", "--iteration", str(i),
                  "--output_dir", os.path.join(path, f"CG-MD-{i}"),
                  "--pdb_file", os.path.join(path, f"AA-MD-{i}", f"AA-MD-{i}-final.pdb")],
                 f"AA → CG conversion (iteration {i})")

        run_step(["python", "Test_CG.py", "--iteration", str(i), "--path", path, "--platform", platform],
                 f"CG-MD simulation (iteration {i})")

        run_step(["python", "Test_CG_AA.py", "--iteration", str(i), "--path", path],
                 f"CG → AA backmapping (iteration {i})")

    return f"🎉 Multiscale simulation complete for {n_iter} iterations. Results in: {path}"

# LangChain tool wrapper
def multiscale_simulation_tool(input_str: str) -> str:
    # Expecting format: "<pdb_path>, <n_iter>, <platform>, <output_path>"
    try:
        args = [x.strip() for x in input_str.split(",")]
        pdb_path, n_iter, platform, output_path = args
        return multiscale_loop(int(n_iter), output_path, platform, pdb_path)
    except Exception as e:
        return f"Error: {str(e)}. Please provide input as '<pdb_path>, <n_iter>, <platform>, <output_path>'"

simulation_tool = Tool(
    name="MultiscaleSimulationTool",
    func=multiscale_simulation_tool,
    description=(
        "Runs a full multiscale MD simulation workflow. "
        "Input format: '<pdb_path>, <n_iter>, <platform>, <output_path>'. "
        "Example: './downloads/1jd4.pdb, 3, CPU, ./runs/1jd4'"
    )
)

# Agent with just this tool
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    openai_api_key="sk"
)

multiscale_simulation_agent = initialize_agent(
    tools=[simulation_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
