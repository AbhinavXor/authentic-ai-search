import { useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { useTypewriter } from "../hooks/useTypewriter";

const components = {
  a: ({ href, children }) => (
    <a href={href} target="_blank" rel="noreferrer">
      {children}
    </a>
  )
};

/**
 * Renders markdown answers. When `stream` is true the text reveals
 * word-by-word with a blinking cursor, faking a live model even though
 * the backend returns the full answer in one response. Once revealed,
 * `onRevealed` fires so the caller can remember not to replay it.
 */
export default function Markdown({ text, stream, onRevealed }) {
  const { displayed, done } = useTypewriter(text, stream);

  useEffect(() => {
    if (stream && done) onRevealed?.();
  }, [stream, done, onRevealed]);

  return (
    <div className="assistant-answer">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={components}
      >
        {displayed || ""}
      </ReactMarkdown>
      {stream && !done && <span className="type-cursor" aria-hidden="true" />}
    </div>
  );
}
