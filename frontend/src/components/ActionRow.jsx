import { Check, ChevronDown, Copy, RotateCcw, Share2, ThumbsDown, ThumbsUp } from "lucide-react";
import TrustMark from "./TrustMark";

/**
 * Compact, icon-only action bar shown under every assistant answer —
 * completed, stopped, or otherwise. Small grey icons, native hover
 * tooltips via the `.has-tooltip` utility, active state highlighting
 * for like/dislike. No large buttons, no labels.
 */
export default function ActionRow({
  copied,
  onCopy,
  liked,
  disliked,
  onLike,
  onDislike,
  shared,
  onShare,
  canRegenerate,
  onRegenerate,
  verificationStatus,
  detailsOpen,
  onToggleDetails
}) {
  return (
    <div className="assistant-actions">
      <button
        type="button"
        className="icon-action has-tooltip"
        data-tip="Copy"
        onClick={onCopy}
        aria-label="Copy answer"
      >
        {copied ? <Check size={15} /> : <Copy size={15} />}
      </button>

      <button
        type="button"
        className={liked ? "icon-action has-tooltip active" : "icon-action has-tooltip"}
        data-tip="Good response"
        onClick={onLike}
        aria-label="Good response"
        aria-pressed={liked}
      >
        <ThumbsUp size={15} />
      </button>

      <button
        type="button"
        className={disliked ? "icon-action has-tooltip active danger" : "icon-action has-tooltip"}
        data-tip="Bad response"
        onClick={onDislike}
        aria-label="Bad response"
        aria-pressed={disliked}
      >
        <ThumbsDown size={15} />
      </button>

      <button
        type="button"
        className="icon-action has-tooltip"
        data-tip={shared ? "Copied" : "Share"}
        onClick={onShare}
        aria-label="Share answer"
      >
        <Share2 size={15} />
      </button>

      {canRegenerate && (
        <button
          type="button"
          className="icon-action has-tooltip"
          data-tip="Regenerate"
          onClick={onRegenerate}
          aria-label="Regenerate answer"
        >
          <RotateCcw size={15} />
        </button>
      )}

      <TrustMark status={verificationStatus} />

      <button
        type="button"
        className="details-toggle"
        onClick={onToggleDetails}
        aria-expanded={detailsOpen}
      >
        Details
        <ChevronDown size={14} className={detailsOpen ? "chevron rotated" : "chevron"} />
      </button>
    </div>
  );
}
