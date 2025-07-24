import asyncio
import logging
import os

from dotenv import load_dotenv
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    draw_all_possible_flows,
    step,
)
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()


class FunFactEvent(Event):
    fact: str


class FunFactWorkflow(Workflow):
    llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))

    def __post_init__(self) -> None:
        self.add_step(self.generate_fact)
        self.add_step(self.critique_fact)

    @step
    async def generate_fact(self, _: StartEvent) -> FunFactEvent:
        response = await self.llm.acomplete("Tell me an interesting fun fact.")
        fact = response.text
        return FunFactEvent(fact=fact)

    @step
    async def critique_fact(self, event: FunFactEvent) -> StopEvent:
        response = await self.llm.acomplete(f"Critique this fact: {event.fact}")
        critique = response.text
        return StopEvent(result=(event.fact, critique))


async def main() -> None:
    workflow = FunFactWorkflow()
    draw_all_possible_flows(workflow)
    result = await workflow.run()
    for result_obj in result:
        logging.info(result_obj)
        logging.info("__________________________________________________________")


asyncio.run(main())
