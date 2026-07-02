// Three independent strokes, each arriving from a different direction,
// resolving into a single point. That's the whole idea of the product:
// separate sources converge and agree on one verified answer.
// One color, two stroke weights, no fills except the center point — so it
// reads identically at 16px, 24px and 32px with no detail loss.
export function Mark({ size = 22 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        d="M12 3.4V10.6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M4.9 18.6L10.5 12.5"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M19.1 18.6L13.5 12.5"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle cx="12" cy="11.6" r="1.85" fill="currentColor" />
    </svg>
  );
}

export function Wordmark() {
  return (
    <div className="wordmark">
      <span className="wordmark-mark">
        <Mark size={20} />
      </span>
      <span className="wordmark-text">
        Authentic<em>AI</em>
      </span>
    </div>
  );
}
