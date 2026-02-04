# KC Overseas Operations Portal

## Project Structure
- `backend/`: FastAPI Application (Python)
- `frontend/`: React Application (Vite + TypeScript)

## Deployment on Railway

### Backend Service
1. Create a new Service on Railway from this GitHub Repo.
2. Settings > Root Directory: `/backend`
3. Variables:
   - `DATABASE_URL`: (PostgreSQL connection string provided by Railway Postgres plugin)
   - `FRONTEND_URL`: `https://<your-frontend-url>.up.railway.app` (Add this after deploying frontend)
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (Or use Procfile)

### Frontend Service
1. Create a new Service on Railway.
2. Settings > Root Directory: `/frontend`
3. Variables:
   - `VITE_API_URL`: `https://<your-backend-url>.up.railway.app`
4. Build Command: `npm install && npm run build`
5. Start Command: `npm run preview -- --host --port $PORT` (For simple preview) or serve static files via a web server.
   *Recommended for Prod:* Use `npm install -g serve` and Start Command: `serve -s dist -l $PORT`

## Local Development
1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Set DATABASE_URL in .env
   uvicorn app.main:app --reload
   ```
2. **Seed Data:**
   ```bash
   cd backend
   # Ensure DATABASE_URL is set
   python seed_data.py
   ```
3. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
