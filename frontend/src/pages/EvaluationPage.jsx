import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { generateEvaluation } from "../api/evaluationApi";

export default function EvaluationPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const responseId = location.state?.responseId;

  const [status, setStatus] = useState("loading"); // loading | success | error
  const [evaluation, setEvaluation] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!responseId) {
      navigate("/");
      return;
    }

    let cancelled = false;

    async function load() {
      setStatus("loading");
      try {
        const data = await generateEvaluation(responseId);
        if (!cancelled) {
          setEvaluation(data);
          setStatus("success");
        }
      } catch (err) {
        if (!cancelled) {
          setStatus("error");
          setErrorMessage(
            err.message === "Failed to fetch"
              ? "Couldn't reach the server. Check your connection and try again."
              : err.message || "Something went wrong generating your evaluation."
          );
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [responseId, navigate]);

  if (!responseId) {
    return null;
  }

  if (status === "loading") {
    return (
      <div className="min-h-screen bg-[#FAF7F1] flex items-center justify-center px-4">
        <p className="text-[#5B6259]">Evaluating your response…</p>
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
          Evaluation
        </p>
        <h1
          className="text-2xl sm:text-3xl text-[#20241F] mb-8 leading-tight text-center"
          style={{ fontFamily: "'Fraunces', serif" }}
        >
          Your evaluation is ready
        </h1>

        <EvaluationSection title="Lesson Objective Status" content={evaluation.lesson_objective_status} />
        <EvaluationSection title="Communication Analysis" content={evaluation.communication_analysis} />
        <EvaluationSection title="Language Analysis" content={evaluation.language_analysis} />
        <EvaluationSection title="Communication Improvements" content={evaluation.communication_improvements} />
        <EvaluationSection title="Grammar Corrections" content={evaluation.grammar_corrections} />
        <EvaluationSection title="Micro Improvements" content={evaluation.micro_improvements} />
      </main>
    </div>
  );
}

function EvaluationSection({ title, content }) {
  if (!content) return null;

  return (
    <section className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8 mb-5">
      <h2 className="text-sm font-medium tracking-wide text-[#5B6259] uppercase mb-3">
        {title}
      </h2>
      <p className="text-[#20241F] leading-relaxed">{content}</p>
    </section>
  );
}