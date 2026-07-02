import { useRef, useState } from "react";
import { Send, Square, X } from "lucide-react";
import { useAutoGrowTextarea } from "../hooks/useAutoGrowTextarea";

export default function Composer({ sidebarVisible, isPending, onSend, onStop }) {
  const [value, setValue] = useState("");
  const textareaRef = useRef(null);

  useAutoGrowTextarea(textareaRef, value);

  function submit(event) {
    event.preventDefault();
    const clean = value.trim();
    if (!clean || isPending) return;
    setValue("");
    onSend(clean);
  }

  return (
    <form
      className={sidebarVisible ? "chat-input-bar sidebar-open" : "chat-input-bar sidebar-closed"}
      onSubmit={submit}
    >
      <div className="composer">
        <textarea
          ref={textareaRef}
          placeholder="Ask Authentic AI..."
          value={value}
          rows={1}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              submit(event);
            }
          }}
        />

        {value && !isPending && (
          <button
            type="button"
            className="clear-button"
            onClick={() => setValue("")}
            aria-label="Clear message"
          >
            <X size={15} />
          </button>
        )}

        {isPending ? (
          <button
            type="button"
            className="send-button stop"
            onClick={onStop}
            aria-label="Stop generating"
          >
            <Square size={14} />
          </button>
        ) : (
          <button
            type="submit"
            className="send-button"
            disabled={!value.trim()}
            aria-label="Send message"
          >
            <Send size={17} />
          </button>
        )}
      </div>

      <p className="composer-hint">
        Authentic AI checks claims against sources, but can still make mistakes.
      </p>
    </form>
  );
}
