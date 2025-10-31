# Intelligent Customer Support System with LangGraph

This project creates a multi-step, multi-agent customer support automation system using `langgraph`. The system can classify incoming requests, route them to the relevant expert (agent), escalate unresolved situations to a higher level, and add a "Human-in-the-Loop" (human approval) step when necessary.

## Features

* **Triage Agent:** Analyzes the incoming message; determines category (`technical`, `billing`), priority (`high`, `medium`), and sentiment (`negative`, `positive`).
* **Expert Agents:** There are 3 different experts: `TechnicalSupportAgent`, `BillingAgent`, and `GeneralSupportAgent`.
* **Conditional Routing:** The graph flow dynamically changes based on the category, priority, or sentiment of the incoming request.
* **Escalation:** Requests containing negative sentiment, high priority, or keywords like "cancel/refund" are routed to the `EscalationAgent`.
* **Human-in-the-Loop:** The `human_review_node` step simulates critical requests being approved or rejected by a human (via terminal).
* **State Management:** Uses `SupportState` (TypedDict) to carry information like `ticket_id`, `customer_id` throughout the conversation.
* **Memory:** Uses `MemorySaver` to remember the state for each conversation (thread_id).

## Installation

1. **Clone the Repository:**
```bash
    git clone https://github.com/AbdulSametTurkmenoglu/smart_customer_support_system_with_langgarph.git
    cd smart_customer_support_system_with_langgarph
```

2. **Virtual Environment (Recommended):**
```bash
    python -m venv .venv
    # Windows: .\.venv\Scripts\activate
    # macOS/Linux: source .venv/bin/activate
```

3. **Install Required Libraries:**
```bash
    pip install -r requirements.txt
```

4. **Create .env File:**
    Copy the `.env.example` file, rename it to `.env`, and fill it with your `OPENAI_API_KEY`:
```bash
    # Windows
    copy .env.example .env
    
    # macOS / Linux
    cp .env.example .env
```

## Usage

The project includes a sample execution script that tests 3 different scenarios. This script demonstrates how the graph branches into different paths (technical support, refund request, negative sentiment).
```bash
python run_examples.py
```

### Sample Output (Refund Request Scenario)
```
============================================================
 EXAMPLE: Billing Cancellation/Refund (Human-in-the-Loop)
============================================================
--- Node: Triage Agent ---
   [Tool] Ticket created: TKT-20251031143005
  └─ Category: billing
  └─ Priority: medium
  └─ Sentiment: neutral
... Step Completed: triage ...
... Routing: After Triage ...
  └─ Decision: billing
... Step Completed: __start__ ...
--- Node: Billing Agent ---
  └─ Human Required: True
... Step Completed: billing ...
... Routing: Escalation Required? ...
  └─ Decision: ESCALATE (Human approval required)
... Step Completed: __cond__ ...
--- Node: Escalation Agent ---
... Step Completed: escalate ...
... Routing: After Escalation ...
  └─ Decision: HUMAN_REVIEW
... Step Completed: __cond__ ...
--- Node: Human Review (Waiting) ---
  └─ Ticket: TKT-20251031143005
  └─ Last message: Your request has been forwarded to a supervisor...
  └─ Do you approve the request? (y/n): y
  └─ Status: Approved
... Step Completed: human_review ...
... Step Completed: __end__ ...
============================================================
 RESULT: Billing Cancellation/Refund (Human-in-the-Loop)
============================================================
  Ticket ID: TKT-20251031143005
  Category: billing
  Status: resolved_by_human
  Last Message: Your request has been approved by our expert and is being processed. Thank you.
============================================================
```
