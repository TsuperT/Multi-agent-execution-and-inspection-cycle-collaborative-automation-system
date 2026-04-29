import zipfile
import os

files = [
    "main.py", "celery_app.py", "models.py",
    "schemas.py", "config.py", "requirements.txt", "README.md"
]

# 生成README
with open("README.md", "w", encoding="utf-8") as f:
    f.write("""# Multi-Agent System
## Run Steps:
1. Install Redis & Start: `redis-server`
2. Install Deps: `pip install -r requirements.txt`
3. Start Worker: `celery -A celery_app worker --loglevel=info`
4. Start Beat: `celery -A celery_app beat --loglevel=info`
5. Start API: `uvicorn main:app --reload`
""")

# 打包
with zipfile.ZipFile("multi_agent_system.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for f in files:
        if os.path.exists(f):
            zf.write(f)
            print(f"Added: {f}")

print("✅ Packaged to multi_agent_system.zip")