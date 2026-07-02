export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * Every call takes its own AbortSignal. Nothing here is module-level
 * mutable state, so two callers (two chats, two tabs, two components)
 * can never step on each other's requests.
 */
export async function postChat(query, signal) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
    signal
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  return response.json();
}

export async function postFeedback(payload, signal) {
  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  return response.json();
}

export function normalizeErrorMessage(error) {
  const message = String(error?.message || error || "");

  if (message.includes("Failed to fetch")) {
    return "Can't reach the backend right now. Start the FastAPI server and try again.";
  }

  return message;
}
