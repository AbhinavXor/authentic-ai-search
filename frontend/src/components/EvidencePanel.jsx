function EvidencePanel({ evidence }) {
  if (!evidence || evidence.length === 0) {
    return null;
  }

  return (
    <section className="panel">
      <h3>Evidence Summary</h3>

      <div className="evidence-list">
        {evidence.map((item, index) => (
          <div className="evidence-item" key={`${item.domain}-${index}`}>
            <div className="evidence-header">
              <strong>{item.source || "Unknown Source"}</strong>
              <span className={`status-pill ${item.status}`}>
                {item.status}
              </span>
            </div>

            <p className="muted">{item.domain}</p>

            {item.claim && (
              <p>
                <strong>Claim:</strong> {item.claim}
              </p>
            )}

            <div className="mini-grid">
              <span>Authority: {item.authority_score}</span>
              <span>Reputation: {item.reputation_score}</span>
              <span>Feedback: {item.feedback_score}</span>
              <span>Reliability: {item.source_reliability_score}</span>
              <span>Freshness: {item.freshness_score}</span>
              <span>Status: {item.freshness_status}</span>
            </div>

            {item.error && (
              <p className="error-text">
                {item.error}
              </p>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

export default EvidencePanel;