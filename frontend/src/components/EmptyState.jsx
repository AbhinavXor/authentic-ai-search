import { Mark } from "./Logo";

export default function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-state-mark">
        <Mark size={30} />
      </div>
      <h2>What can I verify for you?</h2>
      <p>Ask a question. Every answer is checked against sources before it reaches you.</p>
    </div>
  );
}
