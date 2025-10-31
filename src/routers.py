from typing import Literal
from .state import SupportState


def route_after_triage(state: SupportState) -> Literal["technical", "billing", "general", "escalate"]:
    """Triage sonrası yönlendirme"""
    print("... Yönlendirme: Triage Sonrası ...")

    if state["priority"] == "high" or state["sentiment"] == "negative":
        print(f"  └─ Karar: ESCALATE (Öncelik: {state['priority']}, Duygu: {state['sentiment']})")
        return "escalate"

    print(f"  └─ Karar: {state['issue_category']}")
    return state["issue_category"]


def should_escalate(state: SupportState) -> Literal["escalate", "end"]:
    """Çözülemeyen veya insan gerektiren durumları kontrol et"""
    print("... Yönlendirme: Escalation Gerekli mi? ...")

    if state["requires_human"]:
        print("  └─ Karar: ESCALATE (İnsan onayı gerekli)")
        return "escalate"

    if state["resolution_status"] == "resolved":
        print("  └─ Karar: END (Çözüldü)")
        return "end"

    if len(state["messages"]) > 8:
        print("  └─ Karar: ESCALATE (Mesaj sayısı limiti aşıldı)")
        return "escalate"

    print("  └─ Karar: END (Durum çözülmedi ancak insan onayı gerekmiyor)")
    return "end"


def after_escalation_route(state: SupportState) -> Literal["human_review", "end"]:
    """Escalation sonrası yönlendirme"""
    print("... Yönlendirme: Escalation Sonrası ...")

    if state["requires_human"]:
        print("  └─ Karar: HUMAN_REVIEW")
        return "human_review"

    print("  └─ Karar: END")
    return "end"