'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import FileDropzone from '@/components/FileDropzone';
import AnnotatedText from '@/components/AnnotatedText';
import ResultCard from '@/components/ResultCard';
import SeverityBadge from '@/components/SeverityBadge';
import AnnotationSidePanel from '@/components/AnnotationSidePanel';
import { mockAnalyze } from '@/lib/utils/mock';
import { paletteColor } from '@/lib/utils/palette';
import { Annotation } from '@/components/AnnotatedText';
import { cn } from '@/lib/utils';

export default function AnalyzePage() {
  const t = useTranslations();
  const [text, setText] = useState('');
  const [ran, setRan] = useState(false);
  const [analysis, setAnalysis] = useState(() => mockAnalyze(''));
  const [privateMode, setPrivateMode] = useState(true);
  const [sensitivity, setSensitivity] = useState(3);
  const [selectedAnnotation, setSelectedAnnotation] = useState<Annotation | null>(null);
  const [sidePanelOpen, setSidePanelOpen] = useState(false);
  const counts = analysis.counts;

  const run = () => {
    const r = mockAnalyze(text);
    setAnalysis(r);
    setRan(true);
  };

  const handleAnnotationClick = (annotation: Annotation) => {
    setSelectedAnnotation(annotation);
    setSidePanelOpen(true);
  };

  return (
    <>
      <div className="py-8 grid gap-8 lg:grid-cols-2">
        <section>
          <div className="flex items-center justify-between gap-3 mb-3">
            <h2 className="text-xl font-semibold">{t('app.analyze')}</h2>
            <div className="flex items-center gap-3">
              <label className="inline-flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  className="h-4 w-4"
                  checked={privateMode}
                  onChange={(e) => setPrivateMode(e.target.checked)}
                />
                {t('app.privateMode')}
              </label>
              <details className="relative">
                <summary className="btn-ghost px-3 py-1 rounded-lg cursor-pointer">
                  {t('analyzer.settings')}
                </summary>
                <div className="absolute right-0 mt-2 w-72 glass border rounded-xl p-4 z-10">
                  <div className="flex items-center justify-between">
                    <label className="text-sm">Sensitivity</label>
                    <span className="text-sm font-medium">{sensitivity}</span>
                  </div>
                  <input
                    type="range"
                    min={1}
                    max={5}
                    value={sensitivity}
                    onChange={(e) => setSensitivity(Number(e.target.value))}
                    className="w-full mt-2"
                  />
                  <fieldset className="mt-4 text-sm space-y-2">
                    <legend className="font-medium mb-2">Categories</legend>
                    {['outdated', 'biased', 'offensive', 'incorrect'].map((c) => (
                      <label key={c} className="flex items-center gap-2">
                        <input type="checkbox" defaultChecked className="h-4 w-4" />
                        <span className="capitalize">{c}</span>
                      </label>
                    ))}
                  </fieldset>
                </div>
              </details>
            </div>
          </div>

          <div
            className="glass rounded-xl p-4 border"
            style={{ backgroundColor: paletteColor(0) }}
          >
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={t('analyzer.placeholder') as string}
              rows={12}
              className="w-full resize-none bg-transparent outline-none"
              aria-label="Text to analyze"
            />
            <div className="mt-3 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
              <span>{text.length} chars</span>
              <div className="flex items-center gap-2">
                <button onClick={run} className="btn-primary">
                  {t('analyzer.analyzeBtn')}
                </button>
              </div>
            </div>
          </div>

          <div className="my-6 text-center text-sm text-slate-500 dark:text-slate-400">
            {t('analyzer.or')}
          </div>

          <FileDropzone onFiles={() => {}} bgColor={paletteColor(1)} />
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-3">{t('analyzer.results')}</h2>
          <div className="grid gap-4">
            <div
              className="glass rounded-xl p-4 border"
              style={{ backgroundColor: paletteColor(2) }}
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium">{t('analyzer.summary')}:</span>
                <span className="badge bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-200">
                  outdated: {counts.outdated}
                </span>
                <span className="badge bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-200">
                  biased: {counts.biased}
                </span>
                <span className="badge bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-200">
                  offensive: {counts.offensive}
                </span>
                <span className="badge bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200">
                  incorrect: {counts.incorrect}
                </span>
              </div>
            </div>

            {ran && analysis.results.length === 0 && (
              <div
                className="glass rounded-xl p-6 border text-center"
                style={{ backgroundColor: paletteColor(3) }}
              >
                {t('analyzer.noIssues')}
              </div>
            )}

            {analysis.results.map((r, i) => (
              <ResultCard key={i} r={r} bgColor={paletteColor(i + 3)} />
            ))}

            {text && (
              <div
                className="glass rounded-xl p-4 border"
                style={{ backgroundColor: paletteColor(4) }}
              >
                <AnnotatedText
                  text={text}
                  annotations={analysis.annotations}
                  onAnnotationClick={handleAnnotationClick}
                />
              </div>
            )}
          </div>
        </section>
      </div>
      <AnnotationSidePanel
        annotation={selectedAnnotation}
        open={sidePanelOpen}
        onOpenChange={setSidePanelOpen}
      />
    </>
  );
}
