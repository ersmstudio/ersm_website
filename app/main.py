# Entry point for FastAPI app
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def read_root(): return {'Hello': 'World'}