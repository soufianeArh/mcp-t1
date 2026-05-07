from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import os
from datetime import datetime
import asyncio
load_dotenv(override=True)

##mcp to be intalled (node based)
params = {
      "command": "npx","args": ["-y", "mcp-memory-libsql"],
      "env": {"LIBSQL_URL": "file:./sandbox/soufiane.db"}}
instructions = "You use your entity tools as a persistent memory to store and recall information about your conversations."
request = "My name's Soufiane. I'm an LLM engineer. I'm learning a course about AI Agents, including the incredible MCP protocol. \
MCP is a protocol for connecting agents with tools, resources and prompt templates, and makes it easy to integrate AI agents with capabilities."
model = "gpt-4.1-mini"

async def main():

      async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
            agent = Agent(name="agent", instructions=instructions, model=model, mcp_servers=[mcp_server])
            with trace("conversation"):
                  result = await Runner.run(agent, request)
                  print(result.final_output)
      async with MCPServerStdio(params=params, client_session_timeout_seconds=60) as mcp_server:
            agent = Agent(name="agent", instructions=instructions, model=model, mcp_servers=[mcp_server])
            with trace("conversation"):
                  result = await Runner.run(agent, "Im soufiane what you know about me")
                  print(result.final_output)

asyncio.run(main())