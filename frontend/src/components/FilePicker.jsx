import { useRef, useState } from "react";

const ACCEPTED_TYPE = "application/pdf";

export default function FilePicker({ selectedFile, onFileSelect, disabled }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dropError, setDropError] = useState("");

  function handleFiles(fileList) {
    const file = fileList?.[0];
    if (!file) return;

    const isPdf = file.type === ACCEPTED_TYPE || file.name.toLowerCase().endsWith(".pdf");
    if (!isPdf) {
      setDropError("Only PDF files are supported.");
      return;
    }

    setDropError("");
    onFileSelect(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    handleFiles(e.dataTransfer.files);
  }

  function handleDragOver(e) {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  }

  function handleClick() {
    if (!disabled) inputRef.current?.click();
  }

  function handleKeyDown(e) {
    if ((e.key === "Enter" || e.key === " ") && !disabled) {
      e.preventDefault();
      inputRef.current?.click();
    }
  }

  return (
    <div>
      <div
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-disabled={disabled}
        aria-label="Choose a PDF to upload, or drag one here"
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={() => setIsDragging(false)}
        className={`relative overflow-hidden cursor-pointer select-none border-2 border-dashed rounded-lg px-6 py-10 sm:py-12 flex flex-col items-center justify-center gap-3 text-center transition-colors duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAF7F1] ${
          disabled ? "opacity-50 cursor-not-allowed border-[#DDD5C7]" : ""
        } ${
          isDragging && !disabled
            ? "border-[#3E6259] bg-[#DCE7E1]/40"
            : "border-[#C9BFAC] bg-[#FAF7F1]"
        }`}
      >
        {/* folded page corner — signature detail */}
        <div
          aria-hidden="true"
          className="absolute top-0 right-0 w-7 h-7"
          style={{
            background: "linear-gradient(135deg, transparent 50%, #EFEAE1 50%)",
            boxShadow: "inset -1px 1px 2px rgba(32,36,31,0.15)",
          }}
        />

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          className="hidden"
          disabled={disabled}
          onChange={(e) => handleFiles(e.target.files)}
        />

        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z" stroke="#3E6259" strokeWidth="1.5" />
          <path d="M14 2v6h6" stroke="#3E6259" strokeWidth="1.5" />
        </svg>

        <p className="font-medium text-[#20241F]">
          {selectedFile ? "Choose a different PDF" : "Drop your book here, or click to browse"}
        </p>
        <p className="text-sm text-[#5B6259] font-mono">PDF only</p>
      </div>

      {dropError && (
        <p role="alert" className="mt-2 text-sm text-[#A23B2E]">
          {dropError}
        </p>
      )}

      {selectedFile && (
        <div className="mt-3 flex items-center gap-2 rounded-md border border-[#DDD5C7] bg-[#F0EAE0] px-3 py-2">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true" className="shrink-0">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z" stroke="#20241F" strokeWidth="1.5" />
            <path d="M14 2v6h6" stroke="#20241F" strokeWidth="1.5" />
          </svg>
          <span className="text-sm text-[#20241F] truncate">{selectedFile.name}</span>
        </div>
      )}
    </div>
  );
}