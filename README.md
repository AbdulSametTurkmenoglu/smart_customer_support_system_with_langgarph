# LangGraph ile Akıllı Müşteri Destek Sistemi

Bu proje, `langgraph` kullanarak çok adımlı ve çok ajanlı bir müşteri destek otomasyon sistemi oluşturur. Sistem, gelen talepleri sınıflandırabilir, ilgili uzmana (ajan) yönlendirebilir, çözülemeyen durumları bir üst seviyeye (escalate) taşıyabilir ve gerekirse "Human-in-the-Loop" (insan onayı) adımı ekleyebilir.



##  Özellikler

* **Triage Agent:** Gelen mesajı analiz eder; kategori (`technical`, `billing`), öncelik (`high`, `medium`) ve duygu (`negative`, `positive`) belirler.
* **Uzman Ajanlar:** `TechnicalSupportAgent`, `BillingAgent` ve `GeneralSupportAgent` olmak üzere 3 farklı uzman bulunur.
* **Koşullu Yönlendirme:** Gelen talebin kategorisine, önceliğine veya duygusuna göre grafik akışı dinamik olarak değişir.
* **Escalation (Yükseltme):** Negatif duygu, yüksek öncelik veya "iptal/iade" gibi anahtar kelimeler içeren talepler, `EscalationAgent`'a yönlendirilir.
* **Human-in-the-Loop:** `human_review_node` adımı, kritik taleplerin bir insan tarafından (terminal üzerinden) onaylanmasını veya reddedilmesini simüle eder.
* **Durum (State) Yönetimi:** `SupportState` (TypedDict) kullanarak konuşma boyunca `ticket_id`, `customer_id` gibi bilgileri taşır.
* **Hafıza:** `MemorySaver` kullanarak her konuşma (thread_id) için durumu hatırlar.



## Kurulum

1.  **Depoyu Klonlama:**
    ```bash
    git clone [https://github.com/AbdulSametTurkmenoglu/langgarph-ile-akilli-musteri-destek-sistemi.git](https://github.com/AbdulSametTurkmenoglu/langgarph-ile-akilli-musteri-destek-sistemi.git)
    cd langgarph-ile-akilli-musteri-destek-sistemi
    ```

2.  **Sanal Ortam (Önerilir):**
    ```bash
    python -m venv .venv
    # Windows: .\.venv\Scripts\activate
    # macOS/Linux: source .venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Yükleme:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env Dosyasını Oluşturma:**
    `.env.example` dosyasını kopyalayıp `.env` olarak adlandırın ve içini `OPENAI_API_KEY`'inizle doldurun:
    ```bash
    # Windows
    copy .env.example .env
    
    # macOS / Linux
    cp .env.example .env
    ```

##  Kullanım

Proje, 3 farklı senaryoyu test eden bir örnek çalıştırma script'i içerir. Bu script, grafiğin farklı yollara (teknik destek, iade talebi, negatif duygu) nasıl dallandığını gösterir.

```bash
python run_examples.py
```

### Örnek Çıktı (İade Talebi Senaryosu)

```
============================================================
 ÖRNEK: Faturalama İptal/İade (Human-in-the-Loop)
============================================================

--- Node: Triage Agent ---
   [Tool] Ticket oluşturuldu: TKT-20251031143005
  └─ Kategori: billing
  └─ Öncelik: medium
  └─ Duygu: neutral

... Adım Tamamlandı: triage ...
... Yönlendirme: Triage Sonrası ...
  └─ Karar: billing

... Adım Tamamlandı: __start__ ...

--- Node: Billing Agent ---
  └─ İnsan Gerekli mi: True

... Adım Tamamlandı: billing ...
... Yönlendirme: Escalation Gerekli mi? ...
  └─ Karar: ESCALATE (İnsan onayı gerekli)

... Adım Tamamlandı: __cond__ ...

--- Node: Escalation Agent ---

... Adım Tamamlandı: escalate ...
... Yönlendirme: Escalation Sonrası ...
  └─ Karar: HUMAN_REVIEW

... Adım Tamamlandı: __cond__ ...

--- Node: Human Review (Bekleniyor) ---
  └─ Ticket: TKT-20251031143005
  └─ Son mesaj: Talebinizin bir üst yetkiliye iletildiğini...

  └─ Talebi onaylıyor musunuz? (e/h): e
  └─ Durum: Onaylandı

... Adım Tamamlandı: human_review ...

... Adım Tamamlandı: __end__ ...

============================================================
 SONUÇ: Faturalama İptal/İade (Human-in-the-Loop)
============================================================
  Ticket ID: TKT-20251031143005
  Kategori: billing
  Durum: resolved_by_human

  Son Mesaj: Talebiniz uzmanımız tarafından onaylandı ve işleme alındı. Teşekkür ederiz.
============================================================
```