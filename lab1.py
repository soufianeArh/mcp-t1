from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import os
import asyncio

load_dotenv(override=True)

#makes absolute path
sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
#params of mcp server 
fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}
playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"]}
files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}

#Instructions
instructions = ""
###description
instructions += """
You browse the internet to accomplish your instructions.
You are highly capable at browsing the internet independently to accomplish your task, 
including accepting all cookies and clicking 'not now' as
appropriate to get to the content you need. If one website isn't fruitful, try another. 
Be persistent until you have solved your assignment,
trying different options and sites as needed.
When you need to write files, you do that inside the sandbox folder only.
"""

async def main():
    #Tools of mcp servers

    # async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
    #     fetch_tools = await server.list_tools()
    #     print(fetch_tools)
    # async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
    #     playwright_tools = await server.list_tools()
    #     print(playwright_tools)
    # async with MCPServerStdio(params=files_params,client_session_timeout_seconds=60) as server:
    #     file_tools = await server.list_tools()
    #     print(file_tools)

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as files_server:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as playwrite_server:
            agent = Agent(
                name="inverstigator",
                instructions=instructions,
                model="gpt-4.1-mini",
                mcp_servers=[playwrite_server, files_server]
            )
            with trace("investigate"):
                result = await Runner.run(
                    agent,
                    "Find a great recipe for Banoffee Pie, then summarize it in markdown to banoffee.md",
                    max_turns=20)
                print(result.final_output)


asyncio.run(main())