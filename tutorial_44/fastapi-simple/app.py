from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import os
import platform

app = FastAPI()

# HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Docker Demo App</title>
    <style>
        body {{ 
            font-family: sans-serif;
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ text-align: center; color: #333; }}
        .info {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin-top: 20px; }}
        .info p {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello from Docker!</h1>
        <div class="info">
            <p><strong>현재 시간:</strong> {timestamp}</p>
            <p><strong>호스트명:</strong> {hostname}</p>
            <p><strong>Python 버전:</strong> {python_version}</p>
            <p><strong>운영체제:</strong> {os_info}</p>
        </div>
    </div>
</body>
</html>
'''

@app.get("/", response_class=HTMLResponse)
def hello():
    html_content = HTML_TEMPLATE.format(
        timestamp=datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S'),
        hostname=os.environ.get('HOSTNAME', 'unknown'),
        python_version=platform.python_version(),
        os_info=f"{platform.system()} {platform.release()}"
    )
    return html_content

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api")
def api():
    return {
        "message": "Hello Docker!",
        "timestamp": datetime.now().isoformat(),
        "hostname": os.environ.get('HOSTNAME', 'unknown')
    }
