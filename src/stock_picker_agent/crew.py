from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field

from stock_picker_agent.tools.utils import web_search
from stock_picker_agent.tools.utils import PushNotificationTool, JsonTool
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

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def trending_company_finder(self) -> Agent:
        """Find companies that are trending in the news"""
        return Agent(config=self.agents_config['trending_company_finder'], tools=[web_search, JsonTool()])
    
    @agent
    def financial_researcher(self) -> Agent:
        """Provide detailed research on trending companies"""
        return Agent(config=self.agents_config['financial_researcher'], tools=[web_search, JsonTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        """Pick the best company for investment"""
        return Agent(config=self.agents_config['stock_picker'], tools=[PushNotificationTool(), JsonTool()])
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'], 
                    output_pydantic=TrendingCompaniesList,)

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,)

    @task
    def pick_best_company(self) -> Task:
        return Task(config=self.tasks_config['pick_best_company'],)
    
    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )
            
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            tracing=True)


    