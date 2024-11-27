from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Drony - Image Viewer</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
            h1 { color: #2c3e50; }
            a { text-decoration: none; color: #3498db; font-size: 18px; }
            a:hover { text-decoration: underline; color: #2ecc71; }
        </style>
    </head>
    <body>
        <h1>Drony - Viewer</h1>
        <p><a href="/transmitted">1. 모든 이미지</a></p>
        <p><a href="/detected">2. 인식된 이미지</a></p>
        <p><a href="/result">3. 실종자 위치</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
