from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from accounts import Account
import asyncio


load_dotenv(override=True)
account_params = {"command": "uv", "args": ["run", "mcp-server.py"]}
insttructions = """
you are able to manage an account to a client and anser question about the account
"""
async def main():
      ## re
      async with MCPServerStdio(params=account_params, client_session_timeout_seconds=60) as account_mcp:
            list_tools = await account_mcp.list_tools()
            agent = Agent(
                name="Account bot",
                instructions=insttructions,
                model="gpt-4.1-mini",
                mcp_servers=[account_mcp]
            )
            with trace("account_bot"):
                  result = await Runner.run(
                    agent,
                    "My name is John and my account is  under the name: John Doe, i want to know my balance and holdings",
                    max_turns=20)
                  print(result.final_output)

asyncio.run(main())