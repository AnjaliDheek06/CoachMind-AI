// src/api/evaluationApi.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function generateEvaluation(responseId) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/evaluations/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        response_id: responseId,
      }),
    });
  } catch {
    throw new Error("Failed to fetch");
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Couldn't generate the evaluation. Please try again.");
  }

  return data;
}