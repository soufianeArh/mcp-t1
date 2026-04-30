from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from accounts import Account

load_dotenv(override=True)

account = Account.get("soufiane")
print(account)