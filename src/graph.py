from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import SupportState
from .agents import (
    triage_agent,
    technical_support_agent,
    billing_agent,
    general_support_agent,
    escalation_agent,
    human_review_node
)
from .routers import (
    route_after_triage,
    should_escalate,
    after_escalation_route
)


def create_support_graph():
    """Ana destek sistemi graph'ını oluştur"""
    print("Grafik oluşturuluyor...")

    workflow = StateGraph(SupportState)

    # 1. Tüm node'ları (ajanları) tanımla
    workflow.add_node("triage", triage_agent)
    workflow.add_node("technical", technical_support_agent)
    workflow.add_node("billing", billing_agent)
    workflow.add_node("general", general_support_agent)
    workflow.add_node("escalate", escalation_agent)
    workflow.add_node("human_review", human_review_node)

    # 2. Başlangıç noktasını ayarla
    workflow.set_entry_point("triage")

    # 3. Kenarları (edges) ve koşullu yönlendirmeleri tanımla

    # Triage sonrası yönlendirme
    workflow.add_conditional_edges(
        "triage",
        route_after_triage,
        {
            "technical": "technical",
            "billing": "billing",
            "general": "general",
            "escalate": "escalate"
        }
    )

    # Alt ajanlardan (technical, billing, general) sonra
    workflow.add_conditional_edges(
        "technical",
        should_escalate,
        {"escalate": "escalate", "end": END}
    )
    workflow.add_conditional_edges(
        "billing",
        should_escalate,
        {"escalate": "escalate", "end": END}
    )
    workflow.add_conditional_edges(
        "general",
        should_escalate,
        {"escalate": "escalate", "end": END}
    )

    # Escalation node'dan sonra
    workflow.add_conditional_edges(
        "escalate",
        after_escalation_route,
        {"human_review": "human_review", "end": END}
    )

    # Human review'dan sonra her zaman bitir
    workflow.add_edge("human_review", END)

    # 4. Grafiği derle
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    print("Grafik başarıyla derlendi!")
    return app