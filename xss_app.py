from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI(title="Vuln Lab - XSS")

@app.get("/", response_class=HTMLResponse)
def home(q: str = Query(default="", description="Reflected into HTML without escaping (vulnerable)")):
    # VULNERABLE: user input inserted into HTML directly (no escaping/sanitization)
    html = f"""
    <html>
      <body>
        <h1>XSS Demo</h1>
        <p>Search: {q}</p>
        <form method="get">
          <input name="q" value="{q}">
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
