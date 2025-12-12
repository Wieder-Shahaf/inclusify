'use client';

export type DonutDatum = {
  label: string;
  value: number;
  color: string;
};

export default function DonutChart({
  data,
  size = 260,
  thickness = 22,
  center,
}: {
  data: DonutDatum[];
  size?: number;
  thickness?: number;
  center?: {
    title?: string;
    subtitle?: string;
    titleClassName?: string;
    subtitleClassName?: string;
  };
}) {
  const total = data.reduce((s, d) => s + d.value, 0);
  const radius = (size - thickness) / 2;
  const circumference = 2 * Math.PI * radius;
  let offset = 0;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="block">
        <g transform={`translate(${size / 2}, ${size / 2})`}>
          <circle
            r={radius}
            fill="none"
            stroke="currentColor"
            opacity="0.08"
            strokeWidth={thickness}
          />
          {data.map((d, i) => {
            const frac = d.value / total;
            const len = circumference * frac;
            const dashArray = `${len} ${circumference - len}`;
            const dashOffset = -offset;
            offset += len;
            return (
              <circle
                key={i}
                r={radius}
                fill="none"
                stroke={d.color}
                strokeWidth={thickness}
                strokeDasharray={dashArray}
                strokeDashoffset={dashOffset}
                transform="rotate(-90)"
                strokeLinecap="round"
              />
            );
          })}
        </g>
      </svg>
      {center && (
        <div className="absolute inset-0 grid place-items-center text-center">
          <div>
            {center.title && (
              <div className={center.titleClassName ?? 'text-xl font-extrabold'}>
                {center.title}
              </div>
            )}
            {center.subtitle && (
              <div
                className={
                  center.subtitleClassName ?? 'text-xs text-slate-500 dark:text-slate-400'
                }
              >
                {center.subtitle}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
