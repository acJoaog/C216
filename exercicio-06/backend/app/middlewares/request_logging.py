from fastapi import Request
import time

async def log_requests(request: Request, call_next):
    inicio = time.time()

    # Log da requisição
    print(f"➡️ {request.method} {request.url.path}")

    response = await call_next(request)

    duracao = time.time() - inicio
    
    # Log da resposta
    print(f"⬅️ {response.status_code} {request.method} {request.url.path} - {duracao:.3f}s")

    return response