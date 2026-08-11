const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function generateScenario(lessonId) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/scenarios/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        lesson_id: lessonId,
      }),
    });
  } catch {
    throw new Error("Failed to fetch");
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Couldn't generate a scenario. Please try again.");
  }

  return data;
}