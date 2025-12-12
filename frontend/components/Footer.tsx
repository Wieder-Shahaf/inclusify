export default function Footer() {
  return (
    <footer className="container-px mt-16 pb-10">
      <div className="mx-auto max-w-7xl border-t border-slate-200/60 dark:border-slate-800/60 pt-6 text-sm text-slate-500 dark:text-slate-400">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <p>© {new Date().getFullYear()} Achva LGBT — INCLUSIFY</p>
          <p className="opacity-80">Built with accessibility and inclusion in mind.</p>
        </div>
      </div>
    </footer>
  );
}
