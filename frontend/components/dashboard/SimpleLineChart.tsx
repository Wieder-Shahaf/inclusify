'use client';

import { useMemo } from 'react';

export default function SimpleLineChart({
  data,
  labels,
  color = '#7b61ff',
  height = 240,
  showGrid = true,
  areaOpacity = 0.15,
}: {
  data: number[];
  labels?: string[];
  color?: string;
  height?: number;
  showGrid?: boolean;
  areaOpacity?: number;
}) {
  const { path, area, ticks } = useMemo(() => {
    if (data.length === 0) return { path: '', area: '', ticks: [] as number[] };
    const min = Math.min(...data);
    const max = Math.max(...data);
    const pad = (max - min) * 0.2 || 10;
    const yMin = Math.max(0, Math.floor(min - pad));
    const yMax = Math.ceil(max + pad);

    const width = 800;
    const xStep = width / (data.length - 1 || 1);
    const yScale = (v: number) => {
      const h = height - 24; // padding for axes
      return h - ((v - yMin) / (yMax - yMin)) * h + 12;
    };
    const xScale = (i: number) => i * xStep;

    const d = data.map((v, i) => `${i === 0 ? 'M' : 'L'} ${xScale(i)} ${yScale(v)}`).join(' ');
    const a =
      `M 0 ${yScale(yMin)} ` +
      data.map((v, i) => `L ${xScale(i)} ${yScale(v)}`).join(' ') +
      ` L ${xScale(data.length - 1)} ${yScale(yMin)} Z`;

    const tickCount = 4;
    const ticks = new Array(tickCount + 1)
      .fill(0)
      .map((_, i) => yMin + ((yMax - yMin) * i) / tickCount);

    return { path: d, area: a, ticks };
  }, [data, height]);

  return (
    <div className="w-full overflow-hidden">
      <svg viewBox={`0 0 800 ${height}`} className="w-full h-auto">
        {showGrid &&
          ticks.map((t, i) => (
            <g key={i}>
              <line
                x1="0"
                x2="800"
                y1={12 + (height - 24) - ((height - 24) * i) / (ticks.length - 1)}
                y2={12 + (height - 24) - ((height - 24) * i) / (ticks.length - 1)}
                stroke="currentColor"
                opacity="0.08"
              />
            </g>
          ))}
        <path d={area} fill={color} opacity={areaOpacity} />
        <path d={path} fill="none" stroke={color} strokeWidth="3" />
      </svg>
      {labels && labels.length ? (
        <div className="mt-2 grid grid-cols-12 text-xs text-slate-500 dark:text-slate-400">
          {labels.map((l, i) => (
            <span key={i} className="col-span-1 text-center">
              {l}
            </span>
          ))}
        </div>
      ) : null}
    </div>
  );
}
