import src.config
from src.graph import create_support_graph
from langchain_core.messages import HumanMessage
import uuid


def run_example(name, app, initial_state):
    """Tek bir örnek senaryoyu çalıştırır"""
    print("\n" + "=" * 60)
    print(f" ÖRNEK: {name}")
    print("=" * 60)

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}


    final_state = None
    for chunk in app.stream(initial_state, config):
        node_name, state_update = list(chunk.items())[0]
        print(f"\n... Adım Tamamlandı: {node_name} ...")
        final_state = state_update

    print("\n" + "=" * 60)
    print(f" SONUÇ: {name}")
    print("=" * 60)
    print(f"  Ticket ID: {final_state['ticket_id']}")
    print(f"  Kategori: {final_state['issue_category']}")
    print(f"  Durum: {final_state['resolution_status']}")
    print(f"\n  Son Mesaj: {final_state['messages'][-1].content}")
    print("=" * 60)


def main():
    print("""
     LangGraph Akıllı Müşteri Destek Sistemi
    ==========================================
    """)

    try:
        app = create_support_graph()
    except Exception as e:
        print(f"Hata: Grafik oluşturulamadı: {e}")
        return

    example_1_state = {
        "messages": [HumanMessage(content="Sisteme giriş yapamıyorum, şifremi unuttum.")],
        "customer_id": "CUST-12345",
        "resolution_status": "pending",
        "requires_human": False,
    }
    run_example("Basit Teknik Destek (Çözüldü)", app, example_1_state)

    example_2_state = {
        "messages": [HumanMessage(content="Aboneliğimi iptal etmek ve para iadesi almak istiyorum.")],
        "customer_id": "CUST-67890",
        "resolution_status": "pending",
        "requires_human": False,
    }
    run_example("Faturalama İptal/İade (Human-in-the-Loop)", app, example_2_state)

    example_3_state = {
        "messages": [HumanMessage(content="Hiçbir şey çalışmıyor, bu berbat bir hizmet! Acil yardım edin!")],
        "customer_id": "CUST-11111",
        "resolution_status": "pending",
        "requires_human": False,
    }
    run_example("Negatif Duygu (Direkt Escalation)", app, example_3_state)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nKritik Hata: {e}")