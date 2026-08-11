const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function generateLesson(bookId, pageFrom, pageTo) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/lessons/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        book_id: bookId,
        page_from: pageFrom,
        page_to: pageTo,
      }),
    });
  } catch {
    throw new Error("Failed to fetch");
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Couldn't generate the lesson. Please try again.");
  }

  return data;
}

export async function getLesson(lessonId) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/lessons/${lessonId}`);
  } catch {
    throw new Error("Failed to fetch");
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Couldn't load this lesson.");
  }

  return data;
}