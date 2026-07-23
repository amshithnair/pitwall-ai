import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from pitwall.ai_orchestrator.tools.f1_tools import get_strategy_recommendation, get_tyre_prediction, get_race_state
from pitwall.ai_orchestrator.rag import RAGManager

class F1EngineeringAgent:
    def __init__(self):
        # Allow mock key for tests
        api_key = os.getenv("OPENAI_API_KEY", "mock")
        
        # If running in local mock mode without API key, just use a dummy response
        self.is_mock = api_key == "mock"
        
        if not self.is_mock:
            self.llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=api_key)
            self.rag_manager = RAGManager()
            
            @tool
            def search_f1_rules(query: str) -> str:
                """Searches the FIA F1 Sporting Regulations and internal rulebooks for a given query."""
                return self.rag_manager.search_rules(query)
                
            self.tools = [
                get_strategy_recommendation,
                get_tyre_prediction,
                get_race_state,
                search_f1_rules
            ]
            
            self.agent = initialize_agent(
                self.tools, 
                self.llm, 
                agent=AgentType.OPENAI_FUNCTIONS,
                verbose=True,
                agent_kwargs={
                    "system_message": "You are the PitWall AI Engineering Assistant. Your job is to answer race engineer questions using the provided tools. Always consult the F1 rules if asked about legality."
                }
            )
            
    def chat(self, message: str) -> str:
        if self.is_mock:
            return f"[MOCK MODE] I would use tools to answer: {message}"
        
        try:
            response = self.agent.run(message)
            return response
        except Exception as e:
            return f"Error executing agent: {e}"
