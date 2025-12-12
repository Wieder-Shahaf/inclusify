export const PASTEL_BG = ['#E5D9F2', '#D1E9F6', '#FFF8DE', '#FFEAEA', '#F5EFFF'] as const;

export function paletteColor(index: number): string {
  const i = Math.abs(index) % PASTEL_BG.length;
  return PASTEL_BG[i];
}
