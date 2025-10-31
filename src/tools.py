from datetime import datetime

class MockDatabase:
    """Müşteri ve ticket veritabanı simülasyonu"""

    @staticmethod
    def get_customer_info(customer_id: str) -> dict:
        """Müşteri bilgilerini getir"""
        return {
            "customer_id": customer_id,
            "name": "Ahmet Yılmaz",
            "tier": "premium",
            "account_status": "active",
            "total_tickets": 5,
            "last_interaction": "2024-10-15"
        }

    @staticmethod
    def create_ticket(customer_id: str, category: str, priority: str) -> str:
        """Yeni destek talebi oluştur"""
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"   [Tool] Ticket oluşturuldu: {ticket_id}")
        return ticket_id

    @staticmethod
    def get_knowledge_base(query: str) -> list:
        kb = {
            "şifre": ["Şifrenizi sıfırlamak için 'Şifremi Unuttum' linkine tıklayın"],
            "fatura": ["Faturalarınıza hesap > faturalar bölümünden ulaşabilirsiniz"],
            "iptal": ["İptal işlemi için müşteri hizmetleriyle iletişime geçin"]
        }
        for key, docs in kb.items():
            if key in query.lower():
                return docs
        return []

class SentimentAnalyzer:
    """Duygu analizi yapan sınıf"""

    @staticmethod
    def analyze(text: str) -> str:
        negative_words = ["kötü", "berbat", "sinir", "öfke", "memnun değil", "çalışmıyor", "hata"]
        positive_words = ["harika", "mükemmel", "teşekkür", "süper"]

        text_lower = text.lower()
        if any(word in text_lower for word in negative_words):
            return "negative"
        elif any(word in text_lower for word in positive_words):
            return "positive"
        return "neutral"