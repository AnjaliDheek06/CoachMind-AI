export default function PageRangeFields({
  pageFrom,
  pageTo,
  totalPages,
  onPageFromChange,
  onPageToChange,
  error,
  disabled,
}) {
  const fromNum = Number(pageFrom) || 0;
  const toNum = Number(pageTo) || 0;
  const barLeft = totalPages ? Math.max(0, Math.min(100, ((fromNum - 1) / totalPages) * 100)) : 0;
  const barWidth =
    totalPages && toNum >= fromNum
      ? Math.max(0, Math.min(100, ((toNum - fromNum + 1) / totalPages) * 100))
      : 0;

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-[#20241F]">Page range</span>
        <span className="text-xs text-[#5B6259] font-mono">1–{totalPages}</span>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-3">
        <label className="block">
          <span className="block text-xs text-[#5B6259] mb-1">From</span>
          <input
            type="number"
            min={1}
            max={totalPages}
            value={pageFrom}
            disabled={disabled}
            onChange={(e) => onPageFromChange(e.target.value)}
            className="w-full rounded-md border border-[#DDD5C7] bg-white px-3 py-2 text-[#20241F] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259]"
          />
        </label>
        <label className="block">
          <span className="block text-xs text-[#5B6259] mb-1">To</span>
          <input
            type="number"
            min={1}
            max={totalPages}
            value={pageTo}
            disabled={disabled}
            onChange={(e) => onPageToChange(e.target.value)}
            className="w-full rounded-md border border-[#DDD5C7] bg-white px-3 py-2 text-[#20241F] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259]"
          />
        </label>
      </div>

      <div className="h-1.5 rounded-full bg-[#EFEAE1] relative overflow-hidden mb-1" aria-hidden="true">
        <div
          className="absolute top-0 bottom-0 bg-[#3E6259] rounded-full"
          style={{ left: `${barLeft}%`, width: `${barWidth}%` }}
        />
      </div>

      {error && (
        <p role="alert" className="mt-2 text-sm text-[#A23B2E]">
          {error}
        </p>
      )}
    </div>
  );
}