import { Check, Loader2 } from "lucide-react";
import { Mark } from "./Logo";
import { THINKING_STEPS } from "../hooks/useChatController";

export default function ThinkingTimeline({ step, onStop }) {
  return (
    <div className="chat-row assistant-row loading-row">
      <div className="assistant-avatar">
        <Mark size={16} />
      </div>

      <div className="assistant-block">
        <div className="thinking-panel">
          {THINKING_STEPS.map((label, index) => {
            const state =
              index < step ? "done" : index === step ? "active" : "pending";

            return (
              <div className={`thinking-step ${state}`} key={label}>
                <span className="thinking-marker">
                  {state === "done" && <Check size={11} />}
                  {state === "active" && (
                    <Loader2 size={11} className="thinking-spin" />
                  )}
                  {state === "pending" && (
                    <span className="thinking-dot" />
                  )}
                </span>
                <p>{label}</p>
              </div>
            );
          })}
        </div>

        <button className="stop-button" onClick={onStop}>
          Stop generating
        </button>
      </div>
    </div>
  );
}
