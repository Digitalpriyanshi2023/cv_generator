# CV Generator - Web App

This project has been restructured into a modern web application with a separate frontend and backend.

## Project Structure
- `public/`: Contains the HTML, CSS, and JavaScript for the user interface (served automatically by Vercel).
- `api/`: Contains the Python backend (Flask) which interacts with Supabase.
- `desktop_app/`: Contains the legacy PyQt6 desktop version.

## Local Development

### 1. Setup Backend
```bash
cd api
pip install -r requirements.txt
```
Create a `.env` file in the `api/` folder (use `.env.example` as a template) and add your Supabase credentials.

### 2. Run the App
```bash
python api/index.py
```
Open `http://localhost:5000` in your browser.

## Deployment to Vercel

1. Install the Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the root directory.
3. Add your `SUPABASE_URL` and `SUPABASE_KEY` as Environment Variables in the Vercel Dashboard.
