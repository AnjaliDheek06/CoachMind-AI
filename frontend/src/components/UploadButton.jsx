export default function UploadButton({ onClick, disabled, isLoading }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      className={`w-full rounded-md py-3 font-medium tracking-wide transition-colors duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAF7F1] flex items-center justify-center gap-2 ${
        disabled || isLoading
          ? "bg-[#DDD5C7] text-[#8A8272] cursor-not-allowed"
          : "bg-[#20241F] text-[#FAF7F1] hover:bg-[#3E6259] cursor-pointer"
      }`}
    >
      {isLoading && (
        <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" opacity="0.25" />
          <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        </svg>
      )}
      {isLoading ? "Reading your pages…" : "Upload book"}
    </button>
  );
}