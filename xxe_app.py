from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
from lxml import etree

app = FastAPI(title="Vuln Lab - XXE")

@app.post("/parse-xml", response_class=PlainTextResponse)
def parse_xml(xml: str = Body(..., media_type="text/plain", description="XML parsed with entity expansion enabled (vulnerable)")):
    # VULNERABLE: entity resolution enabled
    parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
    root = etree.fromstring(xml.encode("utf-8"), parser=parser)

    # Return text content (may include expanded entity content)
    return PlainTextResponse(root.text or "")
