import { useState } from "react";
import UploadCard from "../components/UploadCard";
import { uploadBook } from "../api/api";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | uploading | success | duplicate | error
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  function handleFileSelect(selected) {
    setFile(selected);
    setStatus("idle");
    setErrorMessage("");
  }

  function handleReset() {
    setFile(null);
    setStatus("idle");
    setResult(null);
    setErrorMessage("");
  }

  async function handleUpload() {
    if (!file) {
      setStatus("error");
      setErrorMessage("Choose a PDF before uploading.");
      return;
    }

    setStatus("uploading");
    setErrorMessage("");

    try {
      const data = await uploadBook(file);
      setResult(data);
      setStatus(data.is_duplicate ? "duplicate" : "success");
    } catch (err) {
      setStatus("error");
      setErrorMessage(
        err.message === "Failed to fetch"
          ? "Couldn't reach the server. Check your connection and try again."
          : err.message || "Something went wrong while uploading. Please try again."
      );
    }
  }

  return (
    <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center px-4 py-12 sm:py-20">
      <header className="max-w-md w-full text-center mb-10">
        <h1
          className="text-4xl sm:text-5xl text-[#20241F] mb-2 leading-none tracking-tight"
          style={{ fontFamily: "'Fraunces', serif", fontWeight: 600 }}
        >
          CoachMind
        </h1>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-[#3E6259] mb-5">
          AI Communication Coach
        </p>
        <p className="text-[#20241F] text-base sm:text-lg leading-relaxed font-medium">
          Upload a book. Get a personalized lesson and real practice scenarios
          from the pages you choose.
        </p>
      </header>

      <main className="w-full max-w-md">
        <UploadCard
          file={file}
          status={status}
          result={result}
          errorMessage={errorMessage}
          onFileSelect={handleFileSelect}
          onUpload={handleUpload}
          onReset={handleReset}
        />
      </main>
    </div>
  );
}