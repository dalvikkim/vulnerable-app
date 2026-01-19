import sqlite3
from fastapi import FastAPI, Query

app = FastAPI(title="Vuln Lab - SQL Injection")

def init_db():
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    cur.execute("DELETE FROM users")
    cur.executemany(
        "INSERT INTO users (username, role) VALUES (?, ?)",
        [("alice", "user"), ("bob", "admin"), ("charlie", "user")]
    )
    conn.commit()
    conn.close()

init_db()

@app.get("/users")
def search_users(username: str = Query(default="", description="Used in string-concatenated SQL (vulnerable)")):
    # VULNERABLE: string concatenation in SQL query
    query = f"SELECT id, username, role FROM users WHERE username = '{username}'"
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        return {"query": query, "results": rows}
    finally:
        conn.close()
