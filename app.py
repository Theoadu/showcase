from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
import langsmith as ls

from prompt import SYSTEM_PROMPT
from logger import logger

load_dotenv()

client = MultiServerMCPClient(
    {
        "products": {
            "transport": "streamable_http",
            "url": "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp",
        }
    }
)



import gradio as gr


async def chat(message, history):
    tools = await client.get_tools()

    agent = create_agent(
        "gpt-4o-mini",
        tools,
        system_prompt=SYSTEM_PROMPT,
    )

    try:
        result =  await agent.ainvoke({"messages": history + [HumanMessage(content=message)]})
    except Exception as e:
        logger.error(e)
        yield f'Error: {str(e)}. Kindly try a different request or contact the support team.'
        return


    if message is None:
        yield ''

    yield result["messages"][-1].content


title = 'GHTechCorp Customer Support'
with gr.Blocks(title=title, fill_height=True) as demo:
    gr.Markdown(
        """
        # GHTechCorp Customer Support

        Welcome! I'm your virtual assistant for monitors, computers, printers & accessories.
        """
    )

    gr.ChatInterface(
        fn=chat,
    )

demo.launch(share=True)