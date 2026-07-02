import { useState } from "react";
import { ExternalLink } from "lucide-react";

const TABS = ["Sources", "Evidence", "Scores", "System notes"];

export default function DetailsPanel({ result, feedbackState, onFeedback }) {
  const [tab, setTab] = useState("Sources");

  const rankedSources = result.ranked_sources || [];
  const citations = result.citations || [];
  const evidence = result.evidence_summary || [];

  return (
    <div className="details-panel">
      <div className="details-tabs">
        {TABS.map((label) => (
          <button
            key={label}
            type="button"
            className={tab === label ? "details-tab active" : "details-tab"}
            onClick={() => setTab(label)}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="details-tab-content">
        {tab === "Sources" && (
          <div>
            {rankedSources.length > 0 ? (
              <ol className="ranked-list">
                {rankedSources.map((source, index) => (
                  <li key={`${source.domain}-${index}`}>
                    <span className="ranked-index">
                      {String(source.source_rank || index + 1).padStart(2, "0")}
                    </span>
                    <span>
                      <strong>{source.source || source.title || source.name}</strong>
                      <span className="ranked-domain">{source.domain}</span>
                    </span>
                  </li>
                ))}
              </ol>
            ) : citations.length > 0 ? (
              <ul className="citations-list">
                {citations.map((citation, index) => (
                  <li key={`${citation.url || citation.domain}-${index}`}>
                    <a href={citation.url} target="_blank" rel="noreferrer">
                      {citation.title || citation.source || citation.domain || "Source"}
                      <ExternalLink size={11} />
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="muted">No source data available for this answer.</p>
            )}
          </div>
        )}

        {tab === "Evidence" && (
          <div className="evidence-list">
            {evidence.length > 0 ? (
              evidence.map((item, index) => (
                <div className="evidence-item" key={index}>
                  <div className="evidence-header">
                    <strong>{item.claim || item.title || `Evidence ${index + 1}`}</strong>
                    {item.status && (
                      <span className={`status-pill ${item.status}`}>{item.status}</span>
                    )}
                  </div>
                  {item.summary && <p className="muted">{item.summary}</p>}
                </div>
              ))
            ) : (
              <p className="muted">No evidence details available for this answer.</p>
            )}
          </div>
        )}

        {tab === "Scores" && (
          <div className="metrics-grid">
            <div className="metric-card">
              <span>Trust</span>
              <strong>{result.trust_score ?? "—"}</strong>
            </div>
            <div className="metric-card">
              <span>Confidence</span>
              <strong>{result.confidence_score ?? "—"}</strong>
            </div>
            <div className="metric-card">
              <span>Quality</span>
              <strong>{result.answer_quality_score ?? "—"}</strong>
            </div>
            <div className="metric-card">
              <span>Safety</span>
              <strong>{result.safety_score ?? "—"}</strong>
            </div>
            <div className="metric-card">
              <span>Risk</span>
              <strong>{result.hallucination_risk_score ?? "—"}</strong>
            </div>
            <div className="metric-card">
              <span>Sources verified</span>
              <strong>{result.verified_source_count ?? "—"}</strong>
            </div>
          </div>
        )}

        {tab === "System notes" && (
          <div className="reasoning-block">
            <p>{result.verification_summary || "No system notes for this answer."}</p>
            {result.warning_message && <p className="muted">{result.warning_message}</p>}
            <p className="muted">
              Consensus across sources: {result.consensus_status || "unknown"}
            </p>
          </div>
        )}
      </div>

      <div className="feedback-box">
        <div className="feedback-actions">
          <button type="button" onClick={() => onFeedback("upvote")}>
            Helpful
          </button>
          <button type="button" onClick={() => onFeedback("downvote")}>
            Not helpful
          </button>
          <button type="button" onClick={() => onFeedback("report")}>
            Report
          </button>
        </div>

        {feedbackState?.status === "saved" && (
          <p className="feedback-status">Thanks — feedback saved.</p>
        )}
        {feedbackState?.status === "failed" && (
          <p className="feedback-status failed">Couldn't save feedback.</p>
        )}
      </div>
    </div>
  );
}
