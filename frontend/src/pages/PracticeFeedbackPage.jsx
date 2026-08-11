import { useLocation, useNavigate } from "react-router-dom";

export default function PracticeFeedbackPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const lessonId = location.state?.lessonId;
  const practiceResult = location.state?.practiceResult;

  if (!lessonId || !practiceResult) {
    return null;
  }

  const { evaluation, coaching, practice_complete: practiceComplete } = practiceResult;

  return (
    <div className="min-h-screen bg-[#FAF7F1] flex flex-col items-center px-4 py-12 sm:py-20">
      <main className="w-full max-w-lg">
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-[#3E6259] mb-3 text-center">
          Practice feedback
        </p>
        <h1
          className="text-2xl sm:text-3xl text-[#20241F] mb-8 leading-tight text-center"
          style={{ fontFamily: "'Fraunces', serif" }}
        >
          Here's how it went
        </h1>

        <p className="text-sm font-medium tracking-wide text-[#3E6259] uppercase mb-3 text-center">
          Evaluation
        </p>
        <FeedbackSection title="Lesson Objective" content={evaluation.lesson_objective_status} />
        <FeedbackSection title="Communication" content={evaluation.communication_analysis} />
        <FeedbackSection title="Language" content={evaluation.language_analysis} />
        <FeedbackSection title="Communication Improvements" content={evaluation.communication_improvements} />
        <FeedbackSection title="Grammar" content={evaluation.grammar_corrections} />
        <FeedbackSection title="Micro Improvements" content={evaluation.micro_improvements} />

        <p className="text-sm font-medium tracking-wide text-[#3E6259] uppercase mb-3 mt-8 text-center">
          Coaching
        </p>
        <FeedbackSection title="Key Improvement" content={coaching.key_improvements} />
        <FeedbackSection title="Why It Matters" content={coaching.why_it_matters} />
        <FeedbackSection title="Next Scenario Focus" content={coaching.next_scenario_focus} />

        {practiceComplete ? (
          <PracticeCompleteCard onUploadAnother={() => navigate("/")} />
        ) : (
          <button
            type="button"
            onClick={() => navigate("/scenario", { state: { lessonId } })}
            className="mt-3 w-full rounded-md bg-[#20241F] text-[#FAF7F1] py-3 font-medium hover:bg-[#3E6259] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2"
          >
            Continue to next scenario →
          </button>
        )}
      </main>
    </div>
  );
}

function FeedbackSection({ title, content }) {
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

function PracticeCompleteCard({ onUploadAnother }) {
  return (
    <section className="rounded-xl border border-[#BFD7CC] bg-[#DCE7E1]/50 p-6 sm:p-8 text-center mt-3">
      <div
        aria-hidden="true"
        className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-[#DCE7E1]"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M5 13l4 4L19 7" stroke="#3E6259" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <p className="text-xl text-[#20241F] mb-2" style={{ fontFamily: "'Fraunces', serif" }}>
        Practice complete
      </p>
      <p className="text-sm text-[#5B6259] leading-relaxed max-w-xs mx-auto mb-6">
        You've completed all three practice scenarios for this lesson.
      </p>
      <button
        type="button"
        onClick={onUploadAnother}
        className="w-full rounded-md bg-[#20241F] text-[#FAF7F1] py-3 font-medium hover:bg-[#3E6259] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#3E6259] focus-visible:ring-offset-2"
      >
        Upload another set of pages or book →
      </button>
    </section>
  );
}