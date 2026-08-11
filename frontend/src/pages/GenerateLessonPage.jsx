import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import GenerateLessonCard from "../components/GenerateLessonCard";
import { generateLesson } from "../api/lessonApi";

export default function GenerateLessonPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const book = location.state; // { bookId, fileName, totalPages }

  const [status, setStatus] = useState("idle"); // idle | generating | success | error
  const [errorMessage, setErrorMessage] = useState("");
  const [lesson, setLesson] = useState(null);

  if (!book?.bookId) {
    return (
      <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center justify-center px-4 text-center">
        <p className="text-[#20241F] mb-4">We couldn't find a book to generate a lesson from.</p>
        <button
          type="button"
          onClick={() => navigate("/")}
          className="rounded-md bg-[#20241F] text-[#FAF7F1] px-5 py-2.5 font-medium hover:bg-[#3E6259] transition-colors"
        >
          Back to upload
        </button>
      </div>
    );
  }

  async function handleGenerate(pageFrom, pageTo) {
    setStatus("generating");
    setErrorMessage("");
    try {
      const data = await generateLesson(book.bookId, pageFrom, pageTo);
      setLesson(data);
      setStatus("success");
    } catch (err) {
      setStatus("error");
      setErrorMessage(
        err.message === "Failed to fetch"
          ? "Couldn't reach the server. Check your connection and try again."
          : err.message || "Something went wrong while generating the lesson. Please try again."
      );
    }
  }

  return (
    <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center px-4 py-12 sm:py-20">
      <header className="max-w-md w-full text-center mb-10">
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-[#3E6259] mb-3">
          Step 2 of your workflow
        </p>
        <h1
          className="text-3xl sm:text-4xl text-[#20241F] mb-3 leading-tight"
          style={{ fontFamily: "'Fraunces', serif" }}
        >
          Generate a lesson
        </h1>
        <p className="text-[#5B6259] text-sm sm:text-base leading-relaxed">
          Choose the pages you want to learn from. The AI will read them and
          build a structured lesson — objectives, principles, rules, and examples.
        </p>
      </header>

      <main className="w-full max-w-md">
        {status === "success" ? (
          <div className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8 text-center">
            <div
              aria-hidden="true"
              className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-[#DCE7E1]"
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M5 13l4 4L19 7" stroke="#3E6259" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <p className="text-xl text-[#20241F] mb-1" style={{ fontFamily: "'Fraunces', serif" }}>
              Lesson generated successfully
            </p>
            <p className="text-sm text-[#5B6259] mb-6">"{lesson?.heading}" is ready.</p>
            <button
              type="button"
              onClick={() => navigate(`/lesson/${lesson.lesson_id}`)}
              className="w-full rounded-md bg-[#20241F] text-[#FAF7F1] py-3 font-medium hover:bg-[#3E6259] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2"
            >
              Continue to lesson →
            </button>
          </div>
        ) : (
          <GenerateLessonCard
            fileName={book.fileName}
            totalPages={book.totalPages}
            onGenerate={handleGenerate}
            status={status}
            errorMessage={errorMessage}
          />
        )}
      </main>
    </div>
  );
}