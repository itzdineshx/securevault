# SecureVault

SecureVault is a small FastAPI backend and Streamlit frontend for secure file uploads with a simple blockchain-style audit log.

Quick start (local, venv):

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
# Start backend
.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
# In a second terminal start the UI
.venv/bin/streamlit run app.py
```

Run with Docker (recommended for deployment/testing):

```bash
# Build and start both services
docker-compose up --build

# Backend API: http://localhost:8000
# Streamlit UI: http://localhost:8501
```

Environment variables:

- `DATABASE_URL` — SQLAlchemy database URL (defaults to SQLite `sqlite:///./securevault.db`)
- `CORS_ALLOW_ORIGINS` — comma-separated list of allowed CORS origins for the API (defaults to `http://localhost:8501`)
- `BACKEND_URL` — used by the Streamlit UI and tests to locate the backend (defaults to `http://localhost:8000`)

Notes:

- The repo uses SQLite by default for simplicity; for production use a managed database and set `DATABASE_URL` accordingly.
- SQLite requires the file to be persisted between containers; the provided `docker-compose.yml` mounts a local `securevault.db`.

Deploying the backend to Render and the frontend to Streamlit Cloud
---------------------------------------------------------------

1) Push your repository to GitHub.

2) Backend (Render):
    - Create a new Web Service on Render and connect your GitHub repo.
    - Choose the "Docker" environment and point to `Dockerfile.backend`.
    - Set the following Environment Variables in Render:
       - `DATABASE_URL` — e.g. `postgres://user:pass@hostname:5432/dbname` (recommended)
       - `CORS_ALLOW_ORIGINS` — e.g. `https://share.streamlit.io` or your Streamlit app URL
    - Deploy. Render will provide a public HTTPS URL for your backend.

3) Frontend (Streamlit Cloud):
    - On Streamlit Cloud, create a new app and connect the same GitHub repo.
    - Set the "Main file" to `app.py`.
    - In the Streamlit app settings, under "Secrets & config", add:
       - `BACKEND_URL` = `https://<your-render-backend-url>`
    - Deploy. Streamlit will host your UI and provide a public HTTPS URL.

4) Update the Streamlit secrets or environment so the frontend points to the Render backend URL.

Notes:
- Do not commit real credentials. Use Render's dashboard to set secrets.
- For production, use a managed Postgres instance and S3-compatible storage for `uploads`.
- The sample `render.yaml` and `.env.example` provide templates for configuration.
# 🔐 SecureVault 🔐

<p align="center">
  <img src="https://media.giphy.com/media/l0HlTy9x8FZo0XO1i/giphy.gif" alt="SecureVault Animation" width="300"/>
</p>

SecureVault is a **Streamlit**-based web application for **secure document storage** and **blockchain-based verification**. 🚀
Upload your documents, get cryptographic hashes, and store them on a tamper-proof blockchain powered by a FastAPI backend. View the full history anytime to confirm integrity! 🕵️‍♂️

---

## 📚 Table of Contents

* [✨ Features](#✨-features)
* [🛠️ Tech Stack](#🛠️-tech-stack)
* [📋 Prerequisites](#📋-prerequisites)
* [⚙️ Installation](#⚙️-installation)
* [🔧 Configuration](#🔧-configuration)
* [🚀 Running the App](#🚀-running-the-app)
* [🎯 Usage](#🎯-usage)
* [🗂️ Project Structure](#🗂️-project-structure)
* [🤝 Contributing](#🤝-contributing)
* [📜 License](#📜-license)
* [📞 Contact](#📞-contact)

---

## ✨ Features

* 🔒 **Document Upload**: Securely upload PDF, JPG, JPEG & PNG files.
* ⛓️ **Blockchain Verification**: Records each document hash on-chain for an **immutable** audit trail.
* 🔑 **Military-Grade Encryption**: End-to-end encryption to keep your data confidential.
* 📊 **Audit Log**: Browse a detailed, timestamped blockchain history in a sleek table.
* ⚙️ **Real-time Feedback**: Spinners, success & error messages, and 🎉 balloons upon success!
* 🌗 **Dark/Light Theme**: Toggle seamlessly with Streamlit's built-in theming.

![Working of Blockchain](How_does_a_blockchain_work_Simply_Explained.gif)

## 🛠️ Tech Stack

* **Frontend**: Streamlit 🌐
* **Backend**: FastAPI 🚀
* **Language**: Python 3.10+ 🐍
* **Data**: Pandas for logs 📈
* **HTTP**: `requests` library 🔗

## 📋 Prerequisites

* Python 3.10 or higher 🐍
* `pip` (or `pipenv`/`poetry`) 📦
* Git for cloning the repo 📝

## ⚙️ Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/securevault.git
   cd securevault
   ```
2. **Create and activate venv**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Configuration

1. **Setup FastAPI Backend**

   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. **Update API URL**
   If your backend runs elsewhere, update `http://localhost:8000` in `app.py`.

---

## 🚀 Running the App

```bash
streamlit run app.py
```

> The app launches at `http://localhost:8501` 🔗

---

## 🎯 Usage

1. **📤 Upload Document**

   * Choose “📤 Upload Document” in the sidebar.
   * Select your file (PDF, JPG, PNG).
   * Click **Upload Document** and watch the magic! ✨

2. **📋 Blockchain Log**

   * Choose “📋 Blockchain Log” in the sidebar.
   * Click **🔄 Refresh Log** to see all blocks.
   * Explore the table for timestamps & hashes. 🔍

---

## 🗂️ Project Structure

```
└── securevault/
    ├── README.md
    ├── app.py
    ├── main.py
    ├── requirements.txt
    ├── securevault.db
    ├── test.txt
    ├── test_upload.py
    ├── ui_components.py
    └── utils.py

```

---

## 🤝 Contributing

1. **Fork** the repo 🍴
2. **Create** a branch: `git checkout -b feature/my-feature` 🌱
3. **Commit** your changes: `git commit -m 'Add awesome feature'` 📝
4. **Push**: `git push origin feature/my-feature` 🔼
5. **Open** a PR and let’s collaborate! 💬

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) 🛡️.

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📞 Contact

Have questions or feedback? Reach out! ✉️

* **LinkedIn**: [kirthiga15](https://www.linkedin.com/in/kirthiga15/)
  
---
SecureVault – Secure your documents & trust your data forever! 🎉
*SecureVault – Secure your documents & trust your data forever!* 🎉
