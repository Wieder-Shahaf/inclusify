'use client';

import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

export default function ThemeToggle() {
  const [dark, setDark] = useState(() =>
    typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  );

  useEffect(() => {
    const html = document.documentElement;
    if (dark) {
      html.classList.add('dark');
      html.setAttribute('data-theme', 'dark');
    } else {
      html.classList.remove('dark');
      html.removeAttribute('data-theme');
    }
  }, [dark]);

  useEffect(() => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.classList.add('dark');
      setDark(true);
    }
  }, []);

  return (
    <button
      onClick={() => setDark((d) => !d)}
      className={cn("btn-ghost rounded-full p-2")}
      aria-pressed={dark}
      title="Toggle theme"
    >
      <span className="sr-only">Toggle theme</span>
      {dark ? (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M21.64 13A9 9 0 1111 2.36 7 7 0 0021.64 13z"></path>
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M12 18a6 6 0 100-12 6 6 0 000 12zm0 4a1 1 0 011 1v1a1 1 0 01-2 0v-1a1 1 0 011-1zm0-22a1 1 0 011-1v1a1 1 0 01-2 0V0a1 1 0 011-1zM0 13a1 1 0 011-1h1a1 1 0 010 2H1a1 1 0 01-1-1zm22 0a1 1 0 011-1h1a1 1 0 010 2h-1a1 1 0 01-1-1zM4.22 19.78a1 1 0 011.42 0l.7.7a1 1 0 01-1.42 1.42l-.7-.7a1 1 0 010-1.42zM17.66 6.34a1 1 0 011.42 0l.7.7a1 1 0 01-1.42 1.42l-.7-.7a1 1 0 010-1.42zM4.22 4.22a1 1 0 010 1.42l-.7.7A1 1 0 012.1 4.92l.7-.7a1 1 0 011.42 0zM19.78 19.78a1 1 0 01-1.42 0l-.7-.7a1 1 0 111.42-1.42l.7.7a1 1 0 010 1.42z"></path>
        </svg>
      )}
    </button>
  );
}
