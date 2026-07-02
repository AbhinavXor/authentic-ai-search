import { useEffect, useRef, useState } from "react";

/**
 * Reveals `fullText` word-by-word instead of dumping it in one paint.
 * When `enabled` is false the full text is shown immediately — used for
 * messages that have already been revealed once (e.g. after switching
 * chats and coming back).
 */
export function useTypewriter(fullText, enabled, msPerChunk = 16) {
  const [displayed, setDisplayed] = useState(enabled ? "" : fullText || "");
  const [done, setDone] = useState(!enabled);
  const indexRef = useRef(0);

  useEffect(() => {
    if (!enabled || !fullText) {
      setDisplayed(fullText || "");
      setDone(true);
      return undefined;
    }

    setDisplayed("");
    setDone(false);
    indexRef.current = 0;

    const chunks = fullText.match(/\S+\s*/g) || [fullText];

    const timer = setInterval(() => {
      indexRef.current += 1;
      setDisplayed(chunks.slice(0, indexRef.current).join(""));

      if (indexRef.current >= chunks.length) {
        clearInterval(timer);
        setDone(true);
      }
    }, msPerChunk);

    return () => clearInterval(timer);
    // fullText is treated as stable once a message is created
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fullText, enabled]);

  return { displayed, done };
}
