import asyncio
import logging
import os

from dotenv import load_dotenv
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()

# import llama_index.core
# llama_index.core.set_global_handler("simple")


# Step 1 output
class LearningObjectivesEvent(Event):
    objectives: str


# Step 2 output
class OutlineEvent(Event):
    objectives: str
    outline: str


# Step 3 output
class ActivitySuggestionsEvent(Event):
    objectives: str
    outline: str
    activities: str


# Define the workflow
class LessonPlanWorkflow(Workflow):
    llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))

    def __post_init__(self) -> None:
        self.add_step(self.generate_objectives)
        self.add_step(self.generate_outline)
        self.add_step(self.suggest_activities)
        self.add_step(self.generate_lesson_plan)

    @step
    async def generate_objectives(self, event: StartEvent) -> LearningObjectivesEvent:
        prompt = f"""You're an experienced teacher. Based on the following lesson topic, write 2–3 clear and measurable learning objectives.

        Topic: {event.input}

        Respond with a plain numbered list of objectives.
        """  # noqa: E501
        response = await self.llm.acomplete(prompt)
        return LearningObjectivesEvent(objectives=response.text)

    @step
    async def generate_outline(self, event: LearningObjectivesEvent) -> OutlineEvent:
        prompt = f"""You're designing a lesson plan. Based on the following learning objectives, create a short instructional outline that includes an introduction, two main activities, and a conclusion.

        Learning Objectives:
        {event.objectives}

        Respond with a clear and structured outline.
        """  # noqa: E501
        response = await self.llm.acomplete(prompt)
        return OutlineEvent(objectives=event.objectives, outline=response.text)

    @step
    async def suggest_activities(self, event: OutlineEvent) -> ActivitySuggestionsEvent:
        prompt = f"""You're a lesson planning assistant. Based on the following instructional outline and learning objectives, suggest 2–3 creative and age-appropriate learning activities.

        Learning Objectives:
        {event.objectives}

        Instructional Outline:
        {event.outline}

        Respond with a list of activity suggestions and brief descriptions for each.
        """  # noqa: E501
        response = await self.llm.acomplete(prompt)
        return ActivitySuggestionsEvent(
            objectives=event.objectives, outline=event.outline, activities=response.text
        )

    @step
    async def generate_lesson_plan(self, event: ActivitySuggestionsEvent) -> StopEvent:
        prompt = f"""You're generating a classroom-ready lesson plan using the following components:

        Learning Objectives:
        {event.objectives}

        Instructional Outline:
        {event.outline}

        Suggested Activities:
        {event.activities}

        Write a complete, well-structured lesson plan that a teacher can use. Include headings, formatting, and make the language clear and supportive.
        """  # noqa: E501
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=response.text)


# Run the workflow
async def main() -> None:
    topic_input = "Software system design"
    workflow = LessonPlanWorkflow()
    result = await workflow.run(input=topic_input)
    logging.info("Final Lesson Plan:\n")
    logging.info(result)


asyncio.run(main())
