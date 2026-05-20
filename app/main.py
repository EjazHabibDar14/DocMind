from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='DocMind API', version='1.0.0')

# CORS — required for browser clients to call this API.
# allow_origins=['*'] is fine for local development.
# In production, restrict this to your actual frontend domain.

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# All API routes will be registered here under /api/v1/
# Example: app.include_router(auth.router, prefix='/api/v1')

@app.get('/')
def root():
    return {'message': 'DocMind API is running', 'version': '1.0.0'}