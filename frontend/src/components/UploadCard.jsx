import { useNavigate } from "react-router-dom";
import FilePicker from "./FilePicker";
import UploadButton from "./UploadButton";

export default function UploadCard({
  file,
  status,
  result,
  errorMessage,
  onFileSelect,
  onUpload,
  onReset,
}) {
  const navigate = useNavigate();
  const isUploading = status === "uploading";
  const isDone = status === "success" || status === "duplicate";

  return (
    <div className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8">
      <p className="text-sm font-medium tracking-wide text-[#5B6259] mb-5 uppercase">
        Upload Communication Book
      </p>

      {!isDone && (
        <>
          <FilePicker selectedFile={file} onFileSelect={onFileSelect} disabled={isUploading} />

          {status === "error" && (
            <p
              role="alert"
              className="mt-4 text-sm text-[#A23B2E] bg-[#F5E3DF] border border-[#E3B9AE] rounded-md px-3 py-2"
            >
              {errorMessage}
            </p>
          )}

          <div className="mt-6">
            <UploadButton onClick={onUpload} disabled={!file} isLoading={isUploading} />
          </div>
        </>
      )}

      {isDone && (
        <div>
          <div
            className={`flex items-start gap-3 rounded-md border px-4 py-3.5 ${
              status === "success"
                ? "border-[#BFD7CC] bg-[#DCE7E1]/50"
                : "border-[#DDD5C7] bg-[#F0EAE0]"
            }`}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" className="mt-0.5 shrink-0">
              <path
                d="M5 13l4 4L19 7"
                stroke={status === "success" ? "#3E6259" : "#B5652D"}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <div>
              <p className="text-sm font-medium text-[#20241F]">
                {status === "success" ? "Uploaded successfully" : "Already in your library"}
              </p>
              <p className="text-sm text-[#20241F] mt-1">
                Book: <span className="font-medium">{result?.file_name}</span>
              </p>
              <p className="text-xs text-[#8A8272] font-mono mt-0.5">
                {result?.total_pages} pages
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() =>
              navigate("/generate-lesson", {
                state: {
                  bookId: result?.book_id,
                  fileName: result?.file_name,
                  totalPages: result?.total_pages,
                },
              })
            }
            className="mt-4 w-full rounded-md bg-[#20241F] text-[#FAF7F1] py-3 font-medium hover:bg-[#3E6259] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2"
          >
            Continue →
          </button>

          <button
            type="button"
            onClick={onReset}
            className="mt-3 w-full text-sm text-[#5B6259] hover:text-[#20241F] transition-colors text-center"
          >
            Upload another
          </button>
        </div>
      )}
    </div>
  );
}