import { useCallback, useMemo, useRef, useState } from "react";
import { postChat, postFeedback, normalizeErrorMessage } from "../lib/api";
import { buildChatTitle, getHistoryBucket, wait } from "../lib/format";

// Five calm steps instead of a debug pipeline. Enough to feel like real
// work is happening, not so much that it reads like log output.
export const THINKING_STEPS = [
  "Understanding request",
  "Searching trusted sources",
  "Checking evidence",
  "Verifying answer",
  "Preparing response"
];

const STEP_TICK_MS = 480;
const MIN_VISIBLE_MS = 2400;
const HISTORY_GROUP_ORDER = ["Pinned", "Today", "Yesterday", "Last 7 Days", "Older"];

const STOPPED_ANSWER_TEXT = "Response stopped.";

/**
 * Owns every piece of chat state as its own slice:
 *  - chats        (messages, per conversation)
 *  - activeChatId (which conversation is on screen)
 *  - pending      (per-chat request progress, keyed by chatId)
 *  - feedback     (per-message feedback: { type, status })
 *
 * Nothing here is a module-level singleton. Every consumer of this hook
 * (i.e. every tab, since each tab runs its own React tree) gets its own
 * refs and its own AbortControllers, so a request started in one chat —
 * or one browser tab — can never be cancelled or overwritten by another.
 */
export function useChatController() {
  const [chats, setChats] = useState({});
  const [activeChatId, setActiveChatId] = useState(null);
  const [pending, setPending] = useState({});
  const [feedback, setFeedback] = useState({});
  const [revealed, setRevealed] = useState(() => new Set());

  const controllersRef = useRef({});
  const requestIdsRef = useRef({});
  const stepTimersRef = useRef({});

  const activeChat = activeChatId ? chats[activeChatId] : null;
  const activeMessages = activeChat?.messages || [];
  const activePending = activeChatId ? pending[activeChatId] : null;

  const groupedHistory = useMemo(() => {
    const all = Object.values(chats).sort((a, b) => b.updatedAt - a.updatedAt);
    const buckets = {};

    for (const chat of all) {
      const key = chat.pinned ? "Pinned" : getHistoryBucket(chat.updatedAt);
      if (!buckets[key]) buckets[key] = [];
      buckets[key].push(chat);
    }

    return HISTORY_GROUP_ORDER.filter((label) => buckets[label]?.length).map(
      (label) => ({ label, items: buckets[label] })
    );
  }, [chats]);

  function cleanupRequest(chatId, timer) {
    if (timer) clearInterval(timer);
    delete stepTimersRef.current[chatId];
    delete controllersRef.current[chatId];
    setPending((prev) => {
      if (!(chatId in prev)) return prev;
      const next = { ...prev };
      delete next[chatId];
      return next;
    });
  }

  function appendAssistantMessage(chatId, assistantMessage) {
    setChats((prev) => {
      const existing = prev[chatId];
      if (!existing) return prev;
      return {
        ...prev,
        [chatId]: {
          ...existing,
          messages: [...existing.messages, assistantMessage],
          updatedAt: Date.now()
        }
      };
    });
  }

  const markRevealed = useCallback((messageId) => {
    setRevealed((prev) => {
      if (prev.has(messageId)) return prev;
      const next = new Set(prev);
      next.add(messageId);
      return next;
    });
  }, []);

  const runQuery = useCallback(
    async (rawQuery, targetChatId) => {
      const clean = rawQuery.trim();
      if (!clean) return;

      const chatId = targetChatId || crypto.randomUUID();
      const userMessage = { id: crypto.randomUUID(), role: "user", content: clean };

      setChats((prev) => {
        const existing = prev[chatId];
        return {
          ...prev,
          [chatId]: {
            id: chatId,
            title: existing?.title || buildChatTitle(clean),
            pinned: existing?.pinned || false,
            messages: [...(existing?.messages || []), userMessage],
            updatedAt: Date.now()
          }
        };
      });
      setActiveChatId(chatId);
      setPending((prev) => ({ ...prev, [chatId]: { step: 0 } }));

      const controller = new AbortController();
      controllersRef.current[chatId] = controller;

      const requestId = crypto.randomUUID();
      requestIdsRef.current[chatId] = requestId;

      const startedAt = Date.now();
      const timer = setInterval(() => {
        setPending((prev) => {
          const current = prev[chatId];
          if (!current) return prev;
          const nextStep = Math.min(current.step + 1, THINKING_STEPS.length - 1);
          if (nextStep === current.step) return prev;
          return { ...prev, [chatId]: { step: nextStep } };
        });
      }, STEP_TICK_MS);
      stepTimersRef.current[chatId] = timer;

      let data = null;

      try {
        data = await postChat(clean, controller.signal);
      } catch (error) {
        if (error?.name === "AbortError") {
          // The person hit Stop. Never remove the exchange — show a
          // stopped assistant message with a full action row instead of
          // silently dropping it, and only if a newer request hasn't
          // already superseded this one.
          if (requestIdsRef.current[chatId] === requestId) {
            appendAssistantMessage(chatId, {
              id: crypto.randomUUID(),
              role: "assistant",
              query: clean,
              stopped: true,
              data: {
                answer: STOPPED_ANSWER_TEXT,
                verification_status: "unknown",
                citations: [],
                source_cards: [],
                sources: []
              }
            });
          }
          cleanupRequest(chatId, timer);
          return;
        }

        data = {
          answer: "I couldn't reach the Authentic AI backend just now.",
          verification_status: "unknown",
          is_connection_error: true,
          warning_message: normalizeErrorMessage(error),
          citations: [],
          source_cards: [],
          sources: []
        };
      }

      // A newer request for this same chat superseded this one — drop it.
      if (requestIdsRef.current[chatId] !== requestId) {
        cleanupRequest(chatId, timer);
        return;
      }

      const elapsed = Date.now() - startedAt;
      await wait(Math.max(0, MIN_VISIBLE_MS - elapsed));

      if (requestIdsRef.current[chatId] !== requestId) {
        cleanupRequest(chatId, timer);
        return;
      }

      appendAssistantMessage(chatId, {
        id: crypto.randomUUID(),
        role: "assistant",
        query: clean,
        data
      });

      cleanupRequest(chatId, timer);
    },
    []
  );

  const sendMessage = useCallback(
    (text) => runQuery(text, activeChatId),
    [runQuery, activeChatId]
  );

  const regenerate = useCallback(
    (chatId, previousQuery) => {
      if (!previousQuery || pending[chatId]) return;
      runQuery(previousQuery, chatId);
    },
    [runQuery, pending]
  );

  const stopGeneration = useCallback((chatId) => {
    controllersRef.current[chatId]?.abort();
  }, []);

  const startNewChat = useCallback(() => {
    setActiveChatId(null);
  }, []);

  const openChat = useCallback((chatId) => {
    setActiveChatId(chatId);
  }, []);

  const togglePin = useCallback((chatId) => {
    setChats((prev) => {
      const existing = prev[chatId];
      if (!existing) return prev;
      return { ...prev, [chatId]: { ...existing, pinned: !existing.pinned } };
    });
  }, []);

  const renameChat = useCallback((chatId, title) => {
    const clean = title.trim();
    if (!clean) return;
    setChats((prev) => {
      const existing = prev[chatId];
      if (!existing) return prev;
      return { ...prev, [chatId]: { ...existing, title: clean } };
    });
  }, []);

  const deleteChat = useCallback(
    (chatId) => {
      controllersRef.current[chatId]?.abort();
      cleanupRequest(chatId, stepTimersRef.current[chatId]);

      setChats((prev) => {
        const next = { ...prev };
        delete next[chatId];
        return next;
      });

      setActiveChatId((current) => (current === chatId ? null : current));
    },
    []
  );

  const submitFeedback = useCallback(async (message, feedbackType) => {
    const result = message?.data;
    if (!result) return;

    const firstCitation = result.citations?.[0] || null;

    setFeedback((prev) => ({
      ...prev,
      [message.id]: { type: feedbackType, status: "sending" }
    }));

    try {
      const response = await postFeedback({
        query: message.query || "",
        answer: result.answer,
        feedback_type: feedbackType,
        source_domain: firstCitation ? firstCitation.domain : null,
        source_name: firstCitation ? firstCitation.source : null
      });

      setFeedback((prev) => ({
        ...prev,
        [message.id]: {
          type: feedbackType,
          status: response.status === "success" ? "saved" : "failed"
        }
      }));
    } catch {
      setFeedback((prev) => ({
        ...prev,
        [message.id]: { type: feedbackType, status: "failed" }
      }));
    }
  }, []);

  return {
    chats,
    activeChatId,
    activeChat,
    activeMessages,
    activePending,
    pending,
    groupedHistory,
    feedback,
    revealed,
    markRevealed,
    sendMessage,
    regenerate,
    stopGeneration,
    startNewChat,
    openChat,
    togglePin,
    renameChat,
    deleteChat,
    submitFeedback
  };
}
