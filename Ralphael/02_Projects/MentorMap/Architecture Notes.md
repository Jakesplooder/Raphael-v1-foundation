# MentorMap Architecture Notes

Generated: 2026-06-14

## Folder Structure

- `(root)`: 13 indexed files
- `backend`: 36 indexed files
- `database`: 3 indexed files
- `frontend`: 35 indexed files

## Likely Architecture

- Stack: Node.js / JavaScript, SQL
- Source root: `C:\Users\cyber\Downloads\MentorMap`
- Tests detected: No

## README Signals

### `frontend/README.md`

# React + Vite This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules. Currently, two official plugins are available: - [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh - [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh ## React Compiler The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [th...
### `README.md`

# MentorMap Your roadmap to a new career. Connect with mentors who've made the transition you're dreaming about. ## Project structure - **frontend/** – React (Vite) + Tailwind CSS - **backend/** – Node.js + Express API - **database/** – PostgreSQL schema and migrations - **01–09** – HTML mockups (reference; implemented in React) ## Quick start ### Frontend ```bash cd frontend npm install npm run dev ``` Open [http://localhost:5173](http://localhost:5173). ### Backend (optional; for auth & data) 1. Create a PostgreSQL database and set `DATABASE_URL` in `backend/.env` (see `backend/.env.example`). 2. Run the schema: ```bash psql $DATABASE_URL -f database/schema.sql ``` 3. Start the API: ```...

## Package / Build Signals

### `backend/package.json`

```text
{ "name": "mentormap-backend", "version": "1.0.0", "description": "MentorMap API server", "main": "src/server.js", "type": "module", "scripts": { "start": "node src/server.js", "dev": "node --watch src/server.js", "db:setup": "node src/setup-production-database.js", "db:persistence": "node src/apply-persistence-schema.js", "check": "node --check src/server.js && node --check src/routes/auth.js && node --check src/routes/community.js && node --check src/routes/resources.js && node --check src/routes/sessions.js && node --check src/routes/mentors.js && node --check src/routes/billing.js && node --check src/routes/messages.js" }, "dependencies": { "bcrypt": "^5.1.1", "bcryptjs": "^3.0.3", "cors": "^2.8.6", "dotenv": "^16.4.5", "express": "^4.22.1", "jsonwebtoken": "^9.0.3", "multer": "^2.0.2", "pg": "^8.18.0" } }
```
### `frontend/package.json`

```text
{ "name": "frontend", "private": true, "version": "0.0.0", "type": "module", "scripts": { "dev": "vite", "build": "vite build", "lint": "eslint .", "preview": "vite preview" }, "dependencies": { "axios": "^1.13.5", "react": "^19.2.0", "react-dom": "^19.2.0", "react-router-dom": "^7.13.0" }, "devDependencies": { "@eslint/js": "^9.39.1", "@tailwindcss/postcss": "^4.1.18", "@types/react": "^19.2.5", "@types/react-dom": "^19.2.3", "@vitejs/plugin-react": "^5.1.1", "autoprefixer": "^10.4.24", "eslint": "^9.39.1", "eslint-plugin-react-hooks": "^7.0.1", "eslint-plugin-react-refresh": "^0.4.24", "globals": "^16.5.0", "postcss": "^8.5.6", "tailwindcss": "^4.1.18", "vite": "^7.2.4" } }
```
