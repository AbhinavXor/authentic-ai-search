function CitationsPanel({ citations }) {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <section className="panel">
      <h3>Citations</h3>

      <ol className="citations-list">
        {citations.map((citation, index) => (
          <li key={`${citation.domain}-${index}`}>
            <a
              href={citation.url}
              target="_blank"
              rel="noreferrer"
            >
              {citation.source}
            </a>

            <p className="muted">
              {citation.domain} · Authority {citation.authority_score} ·
              Reputation {citation.reputation_score}
            </p>
          </li>
        ))}
      </ol>
    </section>
  );
}

export default CitationsPanel;