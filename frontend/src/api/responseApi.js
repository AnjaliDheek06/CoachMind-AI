const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function submitResponse(scenarioId, content) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/responses/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scenario_id: scenarioId,
        content,
      }),
    });
  } catch {
    throw new Error("Failed to fetch");
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Couldn't submit your response. Please try again.");
  }

  return data;
}