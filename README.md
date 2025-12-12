# INCLUSIFY

Monorepo structure:
- frontend/ _ web UI (Next.js + TypeScript)
- backend/ _ API service
- ml/ _ training + inference
- shared/ _ shared schemas/utils
- infra/ _ deployment + docker
- docs/ _ requirements, architecture, threat model

## Quick start

### Frontend Development

From the root directory:
```bash
npm run dev
```

Or from the frontend directory:
```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Frontend Features

- **Next.js 16** with App Router
- **TypeScript** for type safety
- **Tailwind CSS v4** for styling
- **next-intl** for internationalization (English & Hebrew with RTL support)
- **shadcn/ui** for accessible components
- **Text highlights** with clickable annotations that open a side panel

### Available Scripts

From root:
- `npm run dev` - Start frontend development server
- `npm run build` - Build frontend for production
- `npm run start` - Start frontend production server
- `npm run lint` - Lint frontend code
- `npm run frontend:dev` - Explicitly run frontend dev (same as `npm run dev`)
- `npm run frontend:build` - Explicitly build frontend
- `npm run frontend:start` - Explicitly start frontend
- `npm run frontend:lint` - Explicitly lint frontend

### Project Structure

```
frontend/
├── app/[locale]/          # Locale-based routing (en, he)
│   ├── page.tsx          # Home page
│   ├── analyze/          # Text analysis page
│   ├── glossary/         # Glossary page
│   └── admin/            # Admin dashboard
├── components/           # React components
├── i18n/                 # Internationalization config
├── messages/             # Translation files (en.json, he.json)
└── lib/                  # Utilities
```

