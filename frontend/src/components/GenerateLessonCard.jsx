import { useState } from "react";
import PageRangeFields from "./PageRangeFields";

export default function GenerateLessonCard({ totalPages, onGenerate, status, errorMessage }) {
  const [pageFrom, setPageFrom] = useState("1");
  const [pageTo, setPageTo] = useState(String(totalPages || 1));
  const [validationError, setValidationError] = useState("");

  const isGenerating = status === "generating";

  function validate() {
    if (!pageFrom || !pageTo) return "Enter both a start and end page.";
    const from = Number(pageFrom);
    const to = Number(pageTo);
    if (!Number.isInteger(from) || !Number.isInteger(to)) return "Page numbers must be whole numbers.";
    if (from < 1) return "Starting page must be at least 1.";
    if (to > totalPages) return `Ending page can't be greater than ${totalPages}.`;
    if (from > to) return "Starting page can't be greater than the ending page.";
    return "";
  }

  function handleSubmit() {
    const validation = validate();
    setValidationError(validation);
    if (validation) return;
    onGenerate(Number(pageFrom), Number(pageTo));
  }

  return (
    <div className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8">
      <PageRangeFields
        pageFrom={pageFrom}
        pageTo={pageTo}
        totalPages={totalPages}
        onPageFromChange={setPageFrom}
        onPageToChange={setPageTo}
        error={validationError}
        disabled={isGenerating}
      />

      {status === "error" && (
        <p
          role="alert"
          className="mt-4 text-sm text-[#A23B2E] bg-[#F5E3DF] border border-[#E3B9AE] rounded-md px-3 py-2"
        >
          {errorMessage}
        </p>
      )}

      <button
        type="button"
        onClick={handleSubmit}
        disabled={isGenerating}
        aria-busy={isGenerating}
        className={`mt-6 w-full rounded-md py-3 font-medium tracking-wide transition-colors duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAF7F1] flex items-center justify-center gap-2 ${
          isGenerating
            ? "bg-[#DDD5C7] text-[#8A8272] cursor-not-allowed"
            : "bg-[#20241F] text-[#FAF7F1] hover:bg-[#3E6259] cursor-pointer"
        }`}
      >
        {isGenerating && (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" opacity="0.25" />
            <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
          </svg>
        )}
        {isGenerating ? "AI is analyzing your selected pages…" : "Generate lesson"}
      </button>
    </div>
  );
}