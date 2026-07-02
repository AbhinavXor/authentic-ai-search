import { useState } from "react";
import { Mark } from "./Logo";
import ActionRow from "./ActionRow";
import SourceStrip from "./SourceStrip";
import Markdown from "./Markdown";
import DetailsPanel from "./DetailsPanel";

export function UserMessage({ message }) {
  return (
    <div className="chat-row user-row">
      <div className="user-bubble">{message.content}</div>
    </div>
  );
}

export function AssistantMessage({
  message,
  isLast,
  chatIsPending,
  revealed,
  markRevealed,
  onRegenerate,
  onFeedback,
  feedbackStatus
}) {
  const [copied, setCopied] = useState(false);
  const [shared, setShared] = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const result = message.data || {};

  const alreadyRevealed = revealed.has(message.id);
  const shouldStream = isLast && !alreadyRevealed;

  const liked = feedbackStatus?.type === "upvote" && feedbackStatus.status !== "failed";
  const disliked = feedbackStatus?.type === "downvote" && feedbackStatus.status !== "failed";
  const canRegenerate = isLast && !chatIsPending && Boolean(message.query);

  async function copyAnswer() {
    try {
      await navigator.clipboard.writeText(result.answer || "");
      setCopied(true);
      setTimeout(() => setCopied(false), 1400);
    } catch {
      setCopied(false);
    }
  }

  async function shareAnswer() {
    const text = result.answer || "";
    if (!text) return;

    if (navigator.share) {
      try {
        await navigator.share({ text, title: "AuthenticAI answer" });
      } catch {
        // person dismissed the native share sheet — nothing to do
      }
      return;
    }

    try {
      await navigator.clipboard.writeText(text);
      setShared(true);
      setTimeout(() => setShared(false), 1400);
    } catch {
      setShared(false);
    }
  }

  return (
    <div className="chat-row assistant-row">
      <div className="assistant-avatar">
        <Mark size={16} />
      </div>

      <div className="assistant-block">
        <SourceStrip result={result} />

        <Markdown
          text={result.answer}
          stream={shouldStream}
          onRevealed={() => markRevealed(message.id)}
        />

        <ActionRow
          copied={copied}
          onCopy={copyAnswer}
          liked={liked}
          disliked={disliked}
          onLike={() => onFeedback(message, "upvote")}
          onDislike={() => onFeedback(message, "downvote")}
          shared={shared}
          onShare={shareAnswer}
          canRegenerate={canRegenerate}
          onRegenerate={() => onRegenerate(message.query)}
          verificationStatus={result.verification_status}
          detailsOpen={detailsOpen}
          onToggleDetails={() => setDetailsOpen((open) => !open)}
        />

        {detailsOpen && (
          <DetailsPanel
            result={result}
            feedbackState={feedbackStatus}
            onFeedback={(type) => onFeedback(message, type)}
          />
        )}
      </div>
    </div>
  );
}
