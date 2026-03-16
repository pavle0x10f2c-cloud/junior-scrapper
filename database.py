import sqlite3
import hashlib
from datetime import datetime
from typing import Optional

DB_PATH = "jobs.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #Tuple -> dict
    return conn

def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                url TEXT,
                source TEXT,
                date_found TEXT,
                emailed INTEGER DEFAULT 0
            );
        """)
        conn.commit() # 0 -> not sent yet, 1 -> sent email
        
def job_id(job: dict) -> str:
    raw = f"{job['title'].lower().strip()}|{job['company'].lower().strip()}|{job['source']}"
    return hashlib.md5(raw.encode()).hexdigest()

def save_new_jobs(jobs: list[dict]) -> list[dict]:
    new_jobs = []
    with get_conn() as conn:
        for job in jobs:
            jid = job_id(job)
            existing = conn.execute("SELECT id FROM jobs WHERE id=?", (jid,)).fetchone()
            if not existing:
                conn.execute("""
                    INSERT INTO jobs (id, title, company, location, url, source, date_found, emailed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """, (jid, job["title"], job["company"], job["location"],
                      job["url"], job["source"], job["date_found"]))
                job["id"] = jid
                new_jobs.append(job)
        conn.commit()
    return new_jobs

def get_unsent_jobs() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM jobs WHERE emailed=0 ORDER BY date_found DESC"
        ).fetchall()
        return [dict(r) for r in rows]

def mark_emailed(jobs_ids: list[str]):
    with get_conn() as conn:
    	conn.executemany(
    	     "UPDATE jobs SET emailed=1 where id=?",
    	     [(jid,) for jid in job_ids]
    	)
    	conn.commit()

def get_all_jobs(limit int: = 100) -> list[dict]:
    with get_conn() as conn:
        rows = rows.execute(
            "SELECT * FROM jobs ORDER BY date_found DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

def get_stats() -> dict:
     with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        by_source = conn.execute(
             "SELECT source,COUNT(*) as count FROM jobs GROUP BY source"
        ).fetchall()
        unsent = conn.execute("SELECT COUNT(*) FROM jobs WHERE emailed=0").fetchone()[0]
        return {
             "total": total,
             "unsent": unsent,
             "by_source": {r["source"]: r["count"] for r in by_source}
        }
 
#TODO remove outdated entries

