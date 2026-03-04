from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


class TrandingCompanies(BaseModel):
    """A comapny that is trending in the news"""
    name: str = Field(description = "The name of the company")
    ticker: str = Field(description = "The stock ticker of the company")
    reason: str = Field(description = "Why the company is trending in the news")

class TrendingCompaniesList(BaseModel):
    """A list of companies that are trending in the news"""
    companies: List[TrandingCompanies] = Field(description = "A list of companies that are trending in the news")

class TrendingCompanyResearch(BaseModel):
    """A detailed research report on a trending company"""
    name: str = Field(description = "The name of the company")
    market_position: str = Field(description = "The company's position in the market")
    future_outlook: str = Field(description = "The future outlook of the company")
    investment_potential: str = Field(description = "The investment potential of the company")

class TrendingCompanyResearchList(BaseModel):
    """A list of detailed research reports on trending companies"""
    research: List[TrendingCompanyResearch] = Field(description = "A list of detailed research reports on trending companies")

@CrewBase
class StockPickerAgent():
    """StockPickerAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPickerAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
