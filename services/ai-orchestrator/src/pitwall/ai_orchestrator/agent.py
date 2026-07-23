import os
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pitwall.ai_orchestrator.providers.openai_provider import OpenAIProvider
from pitwall.ai_orchestrator.tools.f1_tools import get_strategy_recommendation, get_tyre_prediction, get_race_state
from pitwall.ai_orchestrator.rag import RAGManager

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

class F1EngineeringAgent:
    def __init__(self):
        self.provider = OpenAIProvider()
        self.is_mock = os.getenv("OPENAI_API_KEY", "mock") == "mock"
        
        if not self.is_mock:
            self.llm = self.provider.get_chat_model()
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
            
            self.llm_with_tools = self.llm.bind_tools(self.tools)
            
            # LangGraph setup
            workflow = StateGraph(AgentState)
            workflow.add_node("agent", self._call_model)
            workflow.add_node("tools", ToolNode(self.tools))
            
            workflow.set_entry_point("agent")
            workflow.add_conditional_edges(
                "agent",
                self._should_continue,
                {
                    "continue": "tools",
                    "end": END
                }
            )
            workflow.add_edge("tools", "agent")
            
            self.app = workflow.compile()
            
    def _call_model(self, state: AgentState):
        # Provide system context to guide LLM tool usage
        system_msg = "You are the PitWall AI Engineering Assistant. Your job is to answer race engineer questions using the provided tools. Always consult the F1 rules if asked about legality."
        messages = [("system", system_msg)] + list(state["messages"])
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
        
    def _should_continue(self, state: AgentState):
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "continue"
        return "end"
            
    def chat(self, message: str) -> str:
        if self.is_mock:
            return f"[MOCK MODE] LangGraph would use tools to answer: {message}"
            
        try:
            inputs = {"messages": [HumanMessage(content=message)]}
            result = self.app.invoke(inputs)
            return result["messages"][-1].content
        except Exception as e:
            return f"Error executing LangGraph agent: {e}"
