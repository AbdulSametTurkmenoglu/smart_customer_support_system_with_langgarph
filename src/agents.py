from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from .state import SupportState
from .tools import MockDatabase, SentimentAnalyzer



def triage_agent(state: SupportState) -> SupportState:
    """
    İlk sınıflandırma ajanı
    - Sorunun kategorisini belirler
    - Öncelik seviyesini atar
    - Duygu analizini yapar
    """
    print("\n--- Node: Triage Agent ---")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    last_message = state["messages"][-1].content

    category_prompt = f"""
    Aşağıdaki müşteri mesajını analiz et ve kategoriyi belirle.

    Mesaj: {last_message}

    Kategoriler:
    - technical: Teknik sorunlar, hatalar, erişim problemleri
    - billing: Faturalama, ödeme, abonelik sorunları
    - general: Genel sorular, bilgi talepleri

    Sadece kategori adını döndür (technical/billing/general):
    """

    category = llm.invoke(category_prompt).content.strip().lower()
    if category not in ["technical", "billing", "general"]:
        category = "general"

    priority = "medium"
    if "acil" in last_message.lower() or "hemen" in last_message.lower():
        priority = "high"
    elif "çalışmıyor" in last_message.lower() or "hata" in last_message.lower():
        priority = "high"

    sentiment = SentimentAnalyzer.analyze(last_message)

    ticket_id = MockDatabase.create_ticket(
        state["customer_id"],
        category,
        priority
    )

    print(f"  └─ Kategori: {category}")
    print(f"  └─ Öncelik: {priority}")
    print(f"  └─ Duygu: {sentiment}")

    return {
        "issue_category": category,
        "priority": priority,
        "sentiment": sentiment,
        "ticket_id": ticket_id,
        "messages": [AIMessage(
            content=f"Talebiniz {ticket_id} numaralı ticket olarak kaydedildi. {category} ekibine yönlendiriyorum.")]
    }


def technical_support_agent(state: SupportState) -> SupportState:
    """Teknik destek ajanı"""
    print("\n--- Node: Technical Support Agent ---")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    last_message = state["messages"][-2].content
    kb_docs = MockDatabase.get_knowledge_base(last_message)

    context = ""
    if kb_docs:
        context = f"\n\nBilgi Tabanı:\n" + "\n".join(kb_docs)

    prompt = f"""
    Sen bir teknik destek uzmanısın. Müşterinin teknik sorununu çöz.

    Müşteri mesajı: {last_message}
    {context}

    Adım adım çözüm önerisi sun. Net ve anlaşılır ol.
    """

    response = llm.invoke(prompt).content

    is_resolved = "teşekkür" in last_message.lower() or "şifremi unuttum" in last_message.lower()

    print(f"  └─ Çözüm: {'resolved' if is_resolved else 'pending'}")
    return {
        "resolution_status": "resolved" if is_resolved else "pending",
        "messages": [AIMessage(content=response)]
    }


def billing_agent(state: SupportState) -> SupportState:
    """Faturalama destek ajanı"""
    print("\n--- Node: Billing Agent ---")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    customer = MockDatabase.get_customer_info(state["customer_id"])
    last_message = state["messages"][-2].content

    prompt = f"""
    Sen bir faturalama uzmanısın. Müşterinin fatura/ödeme sorununu çöz.

    Müşteri Bilgileri:
    - Seviye: {customer['tier']}
    - Durum: {customer['account_status']}

    Müşteri mesajı: {last_message}

    Profesyonel ve yardımcı bir yanıt ver. Gerekirse hesap detaylarını kontrol et.
    """
    response = llm.invoke(prompt).content
    requires_human = "iptal" in last_message.lower() or "iade" in last_message.lower()

    print(f"  └─ İnsan Gerekli mi: {requires_human}")
    return {
        "requires_human": requires_human,
        "resolution_status": "pending" if requires_human else "resolved",
        "messages": [AIMessage(content=response)]
    }


def general_support_agent(state: SupportState) -> SupportState:
    """Genel destek ajanı"""
    print("\n--- Node: General Support Agent ---")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    last_message = state["messages"][-2].content

    prompt = f"""
    Sen yardımsever bir müşteri temsilcisisin. Müşterinin genel sorusuna yanıt ver.
    Müşteri mesajı: {last_message}
    Dostça ve bilgilendirici bir yanıt ver.
    """
    response = llm.invoke(prompt).content

    return {
        "resolution_status": "resolved",
        "messages": [AIMessage(content=response)]
    }


def escalation_agent(state: SupportState) -> SupportState:
    """Kritik durumlar için yükseltme ajanı"""
    print("\n--- Node: Escalation Agent ---")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    last_ai_message = state["messages"][-1].content

    prompt = f"""
    Bu talep üst seviye inceleme (escalation) gerektiriyor.
    Önceki ajanın cevabı: "{last_ai_message}"

    Ticket ID: {state['ticket_id']}
    Kategori: {state['issue_category']}
    Öncelik: {state['priority']}
    Duygu: {state['sentiment']}

    Müşteriye, talebinin bir üst yetkiliye iletildiğini ve 
    en kısa sürede inceleneceğini belirten profesyonel bir mesaj yaz.
    """
    response = llm.invoke(prompt).content

    return {
        "resolution_status": "escalated",
        "requires_human": True,
        "messages": [AIMessage(content=response)]
    }


def human_review_node(state: SupportState) -> SupportState:
    """İnsan onayı gerektiren durumlar için (Human-in-the-Loop)"""
    print("\n--- Node: Human Review (Bekleniyor) ---")
    print(f"  └─ Ticket: {state['ticket_id']}")
    print(f"  └─ Son mesaj: {state['messages'][-1].content[:100]}...")


    approval = input("\n  └─ Talebi onaylıyor musunuz? (e/h): ").lower()

    if approval == "e":
        print("  └─ Durum: Onaylandı")
        return {
            "resolution_status": "resolved_by_human",
            "messages": [
                AIMessage(content="Talebiniz uzmanımız tarafından onaylandı ve işleme alındı. Teşekkür ederiz.")]
        }
    else:
        print("  └─ Durum: Reddedildi/Yeniden Yönlendirildi")
        return {
            "resolution_status": "escalated_further",
            "messages": [AIMessage(content="Talebiniz ek inceleme için farklı bir birime yönlendirildi.")]
        }