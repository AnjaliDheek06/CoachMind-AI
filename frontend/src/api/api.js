const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function uploadBook(file) {
  const formData = new FormData();
  formData.append("file", file);

  let response;
  try {
    response = await fetch(`${API_BASE_URL}/upload-book/`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error("Failed to fetch");
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Upload failed. Please try again.");
  }

  return data;
}