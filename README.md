# Faisal-M_EVs_final  

**Electronic Voting System (EVS) with blockchain‑backed vote integrity**  

---  

## Overview  

`Faisal-M_EVs_final` is a Django‑based web application that implements a secure electronic voting platform.  
Key highlights:  

- **Blockchain‑enabled vote storage** – each vote is recorded as an immutable block, guaranteeing tamper‑proof audit trails.  
- **Admin interface** for managing elections, candidates, and voter profiles.  
- **Custom Django forms** for voter registration, login, and ballot casting.  
- **Modular design** – core logic lives in the `EVS` package, making it easy to extend or integrate with other services.  

---  

## Features  

| ✅ | Feature |
|---|---|
| 📊 | **Election Management** – create, edit, and delete elections and candidate lists. |
| 🗳️ | **Secure Ballot Casting** – voters submit votes through Django forms; each vote is hashed and stored in a blockchain block. |
| 🔐 | **User Profiles** – custom `UserProfile` model with email verification and voting status tracking. |
| 🛠️ | **Admin Dashboard** – full CRUD access via Django admin for elections, candidates, and blockchain data. |
| 📜 | **Audit Trail** – immutable `VoteBlock` entries with block hash, previous hash, timestamp, and digital signature. |
| 📦 | **Database Migrations** – ready‑to‑run migration scripts (0️⃣–8️⃣) for setting up the schema. |
| 🧪 | **Extensible Architecture** – separate `blockchain.py`, `forms.py`, `models.py`, and `views.py` for clean separation of concerns. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Framework** | Django 4.x (Python 3.9) |
| **Database** | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| **Blockchain** | Custom lightweight blockchain implementation (`EVS/blockchain.py`) |
| **Front‑end** | Django templates + Bootstrap (optional) |
| **Testing** | Django test framework (unit tests can be added) |
| **Version Control** | Git (GitHub) |

---  

## Installation  

> **Prerequisites** – Python 3.9+, `git`, and a virtual environment tool (`venv` or `conda`).  

1. **Clone the repository**  

   ```bash
   git clone https://github.com/your-username/Faisal-M_EVs_final.git
   cd Faisal-M_EVs_final
   ```

2. **Create and activate a virtual environment**  

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  

   The project uses Django only; you can install it directly or via a `requirements.txt` (create one if missing).  

   ```bash
   pip install Django==4.*
   ```

4. **Configure environment variables**  

   Create a `.env` file (or export variables in your shell) with at least the following:

   ```dotenv
   SECRET_KEY=YOUR_OWN_DJANGO_SECRET_KEY
   DEBUG=True          # Set to False in production
   ```

   > **Note:** Never commit real secret keys to the repository