
# Gmail Intelligence: Recipient Extractor

A high-performance Python-based automation system designed to fetch, sanitize, and extract distinct recipient email IDs from specific senders. Built with the **Gmail API** for reliability and **Streamlit** for a live, interactive execution dashboard featuring real-time state controls.

---

## Quick Start

### 1. Prerequisites
- **Python 3.9+**
- A Google Cloud Project with the **Gmail API** enabled.
- `credentials.json` (OAuth Desktop Client) placed in the root directory.

### 2. Installation
```bash
git clone [https://github.com/kanishkautag/Intern-Assignment.git](https://github.com/kanishkautag/Intern-Assignment.git)
cd Intern-Assignment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

```

### 3. Running the App

```bash
streamlit run main.py

```

---

## Demo

https://github.com/user-attachments/assets/858852c4-3674-44ad-aa3b-8744a0a2ab2f

## Screenshots

<img width="1910" height="906" alt="image" src="https://github.com/user-attachments/assets/ce87266c-0587-4423-8dd9-f91ee383189e" />

---

## Architecture and Design Decisions

### 1. Engine: Gmail API vs. Browser Automation

Instead of using Selenium or Playwright, which are resource-heavy and prone to breakage due to Gmail UI updates, this project utilizes the **Gmail API**.

* **Performance:** API calls are significantly faster than rendering a full DOM.
* **Token Optimization:** The system uses `format='metadata'` to fetch only message headers (`To`, `Cc`, `Bcc`) instead of full message bodies, reducing data transfer and latency.

### 2. Data Integrity and Regex Sanitization

Email headers frequently include display names (e.g., `Name <user@id.com>`).

* **Regex Layer:** A specialized extraction layer isolates only the RFC 5322 compliant email address.
* **Normalization:** All addresses are converted to lowercase and stored in a **Python Set** to guarantee uniqueness and  lookup efficiency.

### 3. Live UI and State Management

To satisfy the requirement for live-tailing logs in Streamlit:

* **Dynamic Table:** Uses `st.empty()` and **Session State** to stream execution steps with color-coded statuses (STARTED, SUCCESS, FAILED, RETRIED) in real-time.
* **Execution Controls:** Implemented a non-blocking state machine allowing users to **Pause**, **Resume**, or **Abort** the automation thread safely.
* **Robust Error Handling:** Includes automated retry logic for authentication and network-sensitive API calls.

---

## Project Structure

```text
Intern-Assignment/
├── main.py              # Streamlit UI, State Machine, and Orchestration
├── .env                 # Local configuration for defaults and limits
├── requirements.txt     # Project dependencies
├── .gitignore           # Excludes secrets and environments
├── credentials.json     # (Local Only) Google API OAuth client secret
├── token.pickle         # (Generated) Local persistent OAuth session token
├── services/
│   ├── __init__.py      # Package initialization
│   ├── gmail_service.py # Core engine: Auth, Fetching, and Regex logic
│   └── logger.py        # UI bridge: Real-time, color-coded logging logic
└── utils/
    └── state_manager.py # Shared execution states for Pause/Abort controls

```

---

## Security and Assumptions

* **Persistence:** Generates a `token.pickle` after the first login, enabling subsequent runs to function without re-authentication.
* **Secret Protection:** Sensitive files (`credentials.json`, `token.pickle`) are strictly excluded from version control to prevent credential leakage.
* **Environment Configuration:** Uses `.env` for configurable parameters like `MAX_RETRIES` and `DEFAULT_SAVE_PATH` to ensure code modularity.
* **Output Safety:** Every export is uniquely timestamped to prevent Windows `PermissionError` conflicts if an existing Excel file is open.

Would you like me to draft the final **Cold Outreach DM** for the founder to send with this link and your resume?

```
