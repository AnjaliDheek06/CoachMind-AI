import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getLesson } from "../api/lessonApi";

export default function LessonPage() {
  const { lessonId } = useParams();
  const navigate = useNavigate();

  const [status, setStatus] = useState("loading"); // loading | success | error
  const [lesson, setLesson] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setStatus("loading");
      try {
        const data = await getLesson(lessonId);
        if (!cancelled) {
          setLesson(data);
          setStatus("success");
        }
      } catch (err) {
        if (!cancelled) {
          setStatus("error");
          setErrorMessage(
            err.message === "Failed to fetch"
              ? "Couldn't reach the server. Check your connection and try again."
              : err.message || "Something went wrong loading this lesson."
          );
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  if (status === "loading") {
    return (
      <div className="min-h-screen bg-[#FAF7F1] flex items-center justify-center px-4">
        <p className="text-[#5B6259]">Loading lesson…</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center justify-center px-4 text-center">
        <p className="text-[#A23B2E] mb-4">{errorMessage}</p>
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

  return (
    <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center px-4 py-12 sm:py-20">
      <main className="w-full max-w-lg">
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-[#3E6259] mb-3 text-center">
          Lesson
        </p>
        <h1
          className="text-2xl sm:text-3xl text-[#20241F] mb-8 leading-tight text-center"
          style={{ fontFamily: "'Fraunces', serif" }}
        >
          {lesson.heading}
        </h1>

        <LessonSection title="Objectives" items={lesson.objectives} />
        <LessonSection title="Principles" items={lesson.principles} />
        <LessonSection title="Rules" items={lesson.rules} />
        <LessonSection title="Examples" items={lesson.examples} />

        <LessonCompletionCard
          onStartPractice={() => navigate("/scenario", { state: { lessonId } })}
        />
      </main>
    </div>
  );
}

function LessonSection({ title, items }) {
  if (!items || items.length === 0) return null;

  return (
    <section className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8 mb-5">
      <h2 className="text-sm font-medium tracking-wide text-[#5B6259] uppercase mb-4">
        {title}
      </h2>
      <ul className="space-y-3">
        {items.map((item, i) => (
          <li key={i} className="flex gap-3 text-[#20241F] leading-relaxed">
            <span className="text-[#3E6259] mt-1 shrink-0" aria-hidden="true">—</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

function LessonCompletionCard({ onStartPractice }) {
  return (
    <section className="rounded-xl border border-[#BFD7CC] bg-[#DCE7E1]/50 p-6 sm:p-8 text-center">
      <div
        aria-hidden="true"
        className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-[#DCE7E1]"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M5 13l4 4L19 7" stroke="#3E6259" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>

      <p className="text-xl text-[#20241F] mb-2" style={{ fontFamily: "'Fraunces', serif" }}>
        Lesson complete
      </p>
      <p className="text-sm text-[#5B6259] leading-relaxed mb-6 max-w-xs mx-auto">
        You've finished this lesson. The next step is to apply what you've
        learned in a realistic professional scenario.
      </p>

      <button
        type="button"
        onClick={onStartPractice}
        className="w-full rounded-md bg-[#20241F] text-[#FAF7F1] py-3 font-medium hover:bg-[#3E6259] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2"
      >
        Start practice →
      </button>
    </section>
  );
}