
# Gmail Intelligence: Recipient Extractor

A high-performance Python-based automation system designed to fetch, sanitize, and extract distinct recipient email IDs from specific senders. Built with the Gmail API for reliability and Streamlit for a live, interactive execution dashboard.


## Quick Start

### 1. Prerequisites

- Python 3.9+
- A Google Cloud Project with the Gmail API enabled
- `credentials.json` (OAuth Desktop Client) placed in the root directory

### 2. Installation

```bash
git clone https://github.com/kanishkautag/Intern-Assignment.git
cd Intern-Assignment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
````

### 3. Running the App

```bash
streamlit run main.py
```

---

## Demo

Add a short demo video or GIF showing the app running.

```
[Place demo video or GIF here]
```

Example:

```md
![Demo](assets/demo.gif)
```

---

## Screenshots

Add UI and output screenshots here.

```
[Place screenshots here]
```

Example:

```md
![Dashboard](assets/dashboard.png)
![Logs](assets/logs.png)
![Output](assets/output.png)
```

---

## Architecture and Design Decisions

### 1. Engine: Gmail API vs Browser Automation

Instead of using Selenium or Playwright, which are resource heavy and prone to breakage due to UI updates, this project uses the Gmail API.

* **Performance:** API calls are significantly faster than rendering a full DOM.
* **Token Optimization:** Uses `format='metadata'` to fetch only message headers (`To`, `Cc`, `Bcc`) instead of full message bodies, minimizing data transfer and latency.

### 2. Data Integrity: Regex Sanitization

Email headers often contain friendly names like `Kanishka <user@gmail.com>`.

* A Regex based extraction layer isolates only RFC 5322 compliant email addresses.
* All addresses are normalized to lowercase and stored in a Python set to guarantee uniqueness with efficiency.

### 3. UI: Live Tailing Logs

Standard Streamlit apps update only after execution completes. To support live logs:

* Uses `st.empty()` with Streamlit Session State to tail logs in real time.
* Provides instant feedback on micro tasks such as `Processing Msg ID: 123...`.

---

## Project Structure

```text
Intern-Assignment/
├── main.py               # Streamlit UI and orchestration logic
├── requirements.txt      # Project dependencies
├── .gitignore            # Excludes secrets from version control
├── credentials.json      # Local Google API OAuth client secret
├── token.pickle          # Local persistent OAuth session token
└── services/
    ├── __init__.py
    ├── gmail_service.py  # Core engine: auth, fetching, regex cleaning
    └── logger.py         # UI bridge: live state management for logs
```

---

## Security and Assumptions

* **Persistence:** Generates `token.pickle` after first login so subsequent runs do not require re authentication.
* **Secret Protection:** Sensitive files like `credentials.json` and `token.pickle` are excluded from version control using `.gitignore`.
* **Output Safety:** To avoid Windows permission errors when Excel files are open, every export is timestamped, for example `recipients_20251223_080000.xlsx`.


