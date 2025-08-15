# app.py
from fastapi import FastAPI, Request, Header, HTTPException
import hmac, hashlib

app = FastAPI()

WEBHOOK_SECRET = "your-secret-here"

def validate_signature(raw_body: bytes, signature_hex: str, secret: str, algo: str = "sha512") -> bool:
    """
    Valida la firma HMAC del body crudo contra el hex enviado en el header.

    :param raw_body: cuerpo crudo tal cual llegó (bytes)
    :param signature_hex: firma en hex SIN prefijo (p.ej. "sha512=" ya removido)
    :param secret: tu secreto compartido
    :param algo: "sha512" o "sha256" (elige según tu emisor)
    """
    algo = algo.lower()
    if algo not in ("sha512", "sha256"):
        raise ValueError("Unsupported HMAC algorithm. Use 'sha512' or 'sha256'.")

    digestmod = hashlib.sha512 if algo == "sha512" else hashlib.sha256
    expected_hex = hmac.new(secret.encode("utf-8"), raw_body, digestmod).hexdigest()

    # Comparación en tiempo constante (strings hex)
    return hmac.compare_digest(expected_hex, signature_hex)

@app.post("/webhooks/genlogs-alerts")
async def genlogs_alerts(
    request: Request,
    signature: str = Header(alias="X-GenLogs-Signature"),
):
    raw = await request.body()
    
    # Extract hex signature from format "sha512=<hex>" 
    signature_hex = signature.split("sha512=")[1] if "sha512=" in signature else signature
    
    if not validate_signature(raw, signature_hex, WEBHOOK_SECRET):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse and display the alert data
    import json
    alert_data = json.loads(raw.decode('utf-8'))
    print("Alert received:", json.dumps(alert_data, indent=2))
    
    return {"ok": True, "alert": alert_data}