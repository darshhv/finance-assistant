import threading
import uvicorn
import subprocess

def run_fastapi():
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)

def run_streamlit():
    subprocess.run(["streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    run_streamlit()
