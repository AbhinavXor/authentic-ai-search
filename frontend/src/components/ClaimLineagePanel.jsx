function ClaimLineagePanel({ lineage }) {
  if (!lineage || lineage.length === 0) {
    return null;
  }

  return (
    <section className="panel">
      <h3>Claim Lineage</h3>

      {lineage.map((item, index) => (
        <div className="lineage-card" key={`${item.claim}-${index}`}>
          <p>
            <strong>Claim:</strong> {item.claim}
          </p>

          <p className="muted">
            Supported by {item.support_count} source(s)
          </p>

          <ul>
            {item.supporting_sources.map((source, sourceIndex) => (
              <li key={`${source.domain}-${sourceIndex}`}>
                <strong>{source.source}</strong> · {source.domain}
                <br />
                Authority {source.authority_score} · Reputation{" "}
                {source.reputation_score} · Status {source.status}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </section>
  );
}

export default ClaimLineagePanel;