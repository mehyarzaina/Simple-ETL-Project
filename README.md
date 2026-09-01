# Simple ETL Project

A lightweight, scheduled ETL (Extract, Transform, Load) pipeline written in Python. It pulls the latest news articles from the [newsdata.io](https://newsdata.io/) API every 2 hours, cleans and normalizes the data, and persists it to a relational database — skipping duplicates along the way.

## How it works

| Stage | What happens | Where |
|---|---|---|
| **Extract** | Calls the newsdata.io `/latest` endpoint and pulls the raw article list | `src/fetch_news.py` |
| **Transform** | Converts list fields (creators, countries) into comma-separated strings and parses publish dates into `datetime` objects | `src/helper.py` |
| **Load** | Inserts new articles (and their categories) into the database via SQLModel, skipping any article that already exists | `src/fetch_news.py` |

The pipeline runs once immediately on startup, then repeats on a schedule (every 2 hours by default) using the `schedule` library.

## Project structure

```
Simple-ETL-Project/
├── src/
│   ├── main.py          # Entry point — sets up the schema and runs the job on a schedule
│   ├── fetch_news.py     # Extract + Load: calls the API and writes records to the DB
│   ├── helper.py         # Transform: field cleanup and date parsing helpers
│   ├── models.py         # SQLModel table definitions (Article, ArticleCategory)
│   └── database.py       # DB engine/session setup
├── requirements.txt
└── .gitignore
```

## Data model

- **Article** — `article_id`, `link`, `title`, `creator`, `language`, `country`, `fetched_at`
- **ArticleCategory** — `category_name`, linked to an `Article` via a one-to-many relationship

## Tech stack

- **Python**
- **SQLModel** / **SQLAlchemy** — ORM and schema definitions
- **Pydantic** — data validation
- **Requests** — API calls
- **Pandas** — data handling
- **schedule** — periodic job scheduling
- **python-decouple** — configuration management


## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mehyarzaina/Simple-ETL-Project.git
cd Simple-ETL-Project
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

The project expects a `config.py` file (or a `.env` file read via `python-decouple`) providing:

```
API_KEY=your_newsdata_io_api_key
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
```

Get a free API key from [newsdata.io](https://newsdata.io/). Both `config.py` and `.env` are excluded from version control via `.gitignore`.

### 4. Run the pipeline

```bash
cd src
python main.py
```

On startup, the pipeline will:
1. Create the database tables if they don't already exist.
2. Fetch and store the latest news articles immediately.
3. Continue running in the background, refreshing the data every 2 hours.

