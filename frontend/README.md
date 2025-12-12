# INCLUSIFY Frontend

LGBTQ+ Inclusive Language Analyzer — Frontend

Responsive, bilingual (EN/HE + RTL), accessible Next.js + TypeScript frontend for an inclusive language analyzer.

## Stack

- **Next.js 16** with App Router
- **TypeScript** for type safety
- **Tailwind CSS v4** (dark mode, responsive)
- **next-intl** (English/Hebrew with RTL support)
- **shadcn/ui** for accessible components
- **Framer Motion** ready (animations can be added)

## Getting Started

First, install dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

**Note:** If Safari shows an HTTPS-Only error, either:
1. Disable HTTPS-Only mode in Safari (Safari → Develop → Disable HTTPS-Only Mode)
2. Or use a different browser like Chrome/Firefox for development

## Features

- **Bilingual Support**: English and Hebrew with full RTL support
- **Text Analysis**: Paste text or upload files for analysis
- **Text Highlights**: Clickable annotations that open a side panel with details
- **Dark Mode**: Theme toggle with system preference detection
- **Accessible**: WCAG-compliant components and semantic HTML
- **Responsive**: Mobile-friendly design

## Project Structure

- `app/[locale]/` - Locale-based routing (en, he)
  - `page.tsx` - Home page with hero and features
  - `analyze/` - Text analysis page with editor and results
  - `glossary/` - Mini glossary/FAQ
  - `admin/` - Admin dashboard with KPIs and charts
- `components/` - React components
  - `AnnotatedText.tsx` - Text with clickable highlights
  - `AnnotationSidePanel.tsx` - Side panel for annotation details
  - `dashboard/` - Dashboard components (KPI cards, charts)
- `i18n/` - Internationalization configuration
- `messages/` - Translation files (en.json, he.json)
- `lib/utils/` - Utilities including mock analyzer

## Fonts

The project uses Google Fonts optimized via `next/font`:
- **Oswald** (weights: 400, 500, 600) - for brand text
- **Raleway** (weights: 400, 600, 700, 800) - for headings
- **Noto Sans Hebrew** (weight: 300) - for Hebrew text

## Notes

- This is the frontend UI. Backend API integration is pending.
- File uploads, reports, and authentication are placeholders.
- Private mode toggle is UI-level only (no storage used here).
- WCAG: color contrast, focus states, and semantic controls included.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [next-intl Documentation](https://next-intl-docs.vercel.app/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
