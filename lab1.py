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






async def main():
    #Tools of mcp servers
    async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
        fetch_tools = await server.list_tools()
        # print(fetch_tools)
    async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
        playwright_tools = await server.list_tools()
        # print(playwright_tools)
    async with MCPServerStdio(params=files_params,client_session_timeout_seconds=60) as server:
        file_tools = await server.list_tools()
        print(file_tools)




asyncio.run(main())