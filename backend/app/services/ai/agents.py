import logging
from typing import List, TypedDict

from langgraph.graph import END, StateGraph

from .orchestrator import AIOrchestrator

logger = logging.getLogger(__name__)
orchestrator = AIOrchestrator()


class ReviewState(TypedDict):
    diff: str
    security_findings: List[dict]
    performance_findings: List[dict]
    architecture_findings: List[dict]
    maintainability_findings: List[dict]
    final_report: str


def security_agent(state: ReviewState):
    logger.info("LangGraph Node: Security Agent")
    findings = orchestrator.run_review("security", state["diff"])
    return {"security_findings": [f.model_dump() for f in findings]}


def performance_agent(state: ReviewState):
    logger.info("LangGraph Node: Performance Agent")
    findings = orchestrator.run_review("performance", state["diff"])
    return {"performance_findings": [f.model_dump() for f in findings]}


def architecture_agent(state: ReviewState):
    logger.info("LangGraph Node: Architecture Agent")
    findings = orchestrator.run_review("architecture", state["diff"])
    return {"architecture_findings": [f.model_dump() for f in findings]}


def maintainability_agent(state: ReviewState):
    logger.info("LangGraph Node: Maintainability Agent")
    findings = orchestrator.run_review("maintainability", state["diff"])
    return {"maintainability_findings": [f.model_dump() for f in findings]}


def final_reviewer(state: ReviewState):
    logger.info("LangGraph Node: Final Reviewer")
    all_findings = (
        state.get("security_findings", [])
        + state.get("performance_findings", [])
        + state.get("architecture_findings", [])
        + state.get("maintainability_findings", [])
    )
    report = f"AI Review Complete. Total unique findings: {len(all_findings)}"
    return {"final_report": report}


def create_review_graph():
    workflow = StateGraph(ReviewState)

    workflow.add_node("security_agent", security_agent)
    workflow.add_node("performance_agent", performance_agent)
    workflow.add_node("architecture_agent", architecture_agent)
    workflow.add_node("maintainability_agent", maintainability_agent)
    workflow.add_node("final_reviewer", final_reviewer)

    workflow.set_entry_point("security_agent")
    workflow.add_edge("security_agent", "performance_agent")
    workflow.add_edge("performance_agent", "architecture_agent")
    workflow.add_edge("architecture_agent", "maintainability_agent")
    workflow.add_edge("maintainability_agent", "final_reviewer")
    workflow.add_edge("final_reviewer", END)

    return workflow.compile()


graph = create_review_graph()


def run_review_workflow(diff: str):
    initial_state = {
        "diff": diff,
        "security_findings": [],
        "performance_findings": [],
        "architecture_findings": [],
        "maintainability_findings": [],
        "final_report": "",
    }
    return graph.invoke(initial_state)
