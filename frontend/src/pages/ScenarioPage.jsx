import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { generateScenario } from "../api/scenarioApi";
import { submitPractice } from "../api/practiceApi";



export default function ScenarioPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const lessonId = location.state?.lessonId;


  const [status, setStatus] = useState("loading"); // loading | success | error
  const [scenario, setScenario] = useState(null);
  const [isResumed, setIsResumed] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const [responseContent, setResponseContent] = useState("");
  const [submitStatus, setSubmitStatus] = useState("idle"); // idle | submitting | error
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    if (!lessonId) {
      navigate("/");
      return;
    }

  

    let cancelled = false;

    async function load() {
      setStatus("loading");
      try {
        const data = await generateScenario(lessonId);
        if (!cancelled) {
          setScenario(data);
          setIsResumed(data.is_resumed);
          setStatus("success");
        }
      } catch (err) {
        if (!cancelled) {
          setStatus("error");
          setErrorMessage(
            err.message === "Failed to fetch"
              ? "Couldn't reach the server. Check your connection and try again."
              : err.message || "Something went wrong preparing your scenario."
          );
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [lessonId, navigate]);

  async function handleSubmitResponse() {
    if (!responseContent.trim()) {
      setSubmitStatus("error");
      setSubmitError("Write a response before submitting.");
      return;
    }

    setSubmitStatus("submitting");
    setSubmitError("");

    try {
      const data = await submitPractice(scenario.scenario_id, responseContent);
      navigate("/practice-feedback", {
        state: {
          lessonId,
          practiceResult: data,
        },
      });
    } catch (err) {
      setSubmitStatus("error");
      setSubmitError(
        err.message === "Failed to fetch"
          ? "Couldn't reach the server. Check your connection and try again."
          : err.message || "Something went wrong submitting your response."
      );
    }
  }

  if (!lessonId) {
    return null;
  }

  if (status === "loading") {
    return (
      <div className="min-h-screen bg-[#FAF7F1] flex items-center justify-center px-4">
        <p className="text-[#5B6259]">Preparing your scenario…</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center justify-center px-4 text-center">
        <p className="text-[#A23B2E] mb-4">{errorMessage}</p>
        <button
          type="button"
          onClick={() => navigate(`/lesson/${lessonId}`)}
          className="rounded-md bg-[#20241F] text-[#FAF7F1] px-5 py-2.5 font-medium hover:bg-[#3E6259] transition-colors"
        >
          Back to lesson
        </button>
      </div>
    );
  }

  const isSubmitting = submitStatus === "submitting";

  return (
    <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center px-4 py-12 sm:py-20">
      <main className="w-full max-w-lg">
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-[#3E6259] mb-3 text-center">
          {isResumed ? "Welcome back!" : "Practice scenario"}
        </p>
        <h1
          className="text-2xl sm:text-3xl text-[#20241F] mb-3 leading-tight text-center"
          style={{ fontFamily: "'Fraunces', serif" }}
        >
          {isResumed ? "Continue your unfinished practice session" : "Your practice scenario is ready"}
        </h1>

        <section className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8 mt-8">
          
          <h2
            className="text-xl text-[#20241F] mb-4 leading-snug"
            style={{ fontFamily: "'Fraunces', serif" }}
          >
            {scenario.title}
          </h2>

          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium tracking-wide text-[#5B6259] uppercase mb-1">
                Context
              </p>
              <p className="text-[#20241F] leading-relaxed">{scenario.context}</p>
            </div>
            <div>
              <p className="text-sm font-medium tracking-wide text-[#5B6259] uppercase mb-1">
                Your goal
              </p>
              <p className="text-[#20241F] leading-relaxed">{scenario.objective}</p>
            </div>
          </div>
        </section>

        <section className="rounded-xl border border-[#DDD5C7] bg-white/60 backdrop-blur-sm shadow-sm p-6 sm:p-8 mt-5">
          <label htmlFor="response" className="block text-sm font-medium tracking-wide text-[#5B6259] uppercase mb-3">
            Your response
          </label>
          <textarea
            id="response"
            value={responseContent}
            onChange={(e) => setResponseContent(e.target.value)}
            disabled={isSubmitting}
            rows={8}
            placeholder="Write how you'd respond in this situation…"
            className="w-full rounded-md border border-[#DDD5C7] bg-white px-3 py-2.5 text-[#20241F] leading-relaxed resize-y focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] disabled:opacity-50"
          />

          {submitStatus === "error" && (
            <p role="alert" className="mt-3 text-sm text-[#A23B2E] bg-[#F5E3DF] border border-[#E3B9AE] rounded-md px-3 py-2">
              {submitError}
            </p>
          )}

          <button
            type="button"
            onClick={handleSubmitResponse}
            disabled={isSubmitting}
            aria-busy={isSubmitting}
            className={`mt-4 w-full rounded-md py-3 font-medium tracking-wide transition-colors duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAF7F1] flex items-center justify-center gap-2 ${
              isSubmitting
                ? "bg-[#DDD5C7] text-[#8A8272] cursor-not-allowed"
                : "bg-[#20241F] text-[#FAF7F1] hover:bg-[#3E6259] cursor-pointer"
            }`}
          >
            {isSubmitting && (
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" opacity="0.25" />
                <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
              </svg>
            )}
            {isSubmitting ? "Submitting…" : "Submit response →"}
          </button>
        </section>
      </main>
    </div>
  );
}