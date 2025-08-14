from typing import Iterable

def render_clients_table(rows: Iterable[dict]) -> str:
    # ATENCIÓN: No sanitiza los campos -> XSS almacenado
    trs = []
    for r in rows:
        trs.append(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['email']}</td><td>{r.get('notes','')}</td><td>{r['created_at']}</td></tr>")
    table = "<table border='1'><thead><tr><th>id</th><th>name</th><th>email</th><th>notes</th><th>created_at</th></tr></thead><tbody>" + "".join(trs) + "</tbody></table>"
    return f"""<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Clients</title></head>
  <body>
    <h1>Clients (sin sanitizar)</h1>
    {table}
  </body>
</html>"""
