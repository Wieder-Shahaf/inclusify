'use client';

import { useRef } from 'react';
import { cn } from '@/lib/utils';

export default function FileDropzone({
  onFiles,
  bgColor,
}: {
  onFiles: (files: FileList) => void;
  bgColor?: string;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  return (
    <div
      className={cn(
        "glass rounded-xl p-6 text-center border-dashed border-2 border-slate-200 dark:border-slate-800 hover:border-pride-purple/40 transition-colors"
      )}
      style={bgColor ? { backgroundColor: bgColor } : undefined}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') inputRef.current?.click();
      }}
      aria-label="Upload file for analysis"
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.doc,.docx,.txt"
        className="hidden"
        onChange={(e) => {
          if (e.target.files?.length) onFiles(e.target.files);
        }}
      />
      <div className="mx-auto mb-3 h-10 w-10 rounded-full bg-gradient-to-tr from-pride-purple to-pride-pink text-white grid place-items-center shadow-brand">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M12 3l4 4h-3v6h-2V7H8l4-4zM5 18h14v2H5v-2z" />
        </svg>
      </div>
      <p className="font-medium">Click to upload PDF/DOCX</p>
      <p className="text-sm text-slate-500 dark:text-slate-400">Drag & drop also supported</p>
    </div>
  );
}
