import { useState } from "react";
import { ExternalLink, Globe } from "lucide-react";
import { extractDomain, faviconUrl } from "../lib/format";

const VISIBLE_LIMIT = 4;

export default function SourceStrip({ result }) {
  const [showAll, setShowAll] = useState(false);

  const items =
    result?.source_cards?.length > 0
      ? result.source_cards
      : result?.citations?.length > 0
        ? result.citations
        : result?.sources || [];

  if (!items.length) return null;

  const seen = new Set();
  const unique = [];

  for (const item of items) {
    const url = item.url;
    if (!url || seen.has(url)) continue;
    seen.add(url);

    const domain = item.domain || extractDomain(url);

    unique.push({
      title: item.title || item.name || item.source || domain || "Source",
      domain,
      url,
      verified: item.status === "verified" || item.verified === true
    });
  }

  if (!unique.length) return null;

  const visible = showAll ? unique : unique.slice(0, VISIBLE_LIMIT);
  const remaining = unique.length - VISIBLE_LIMIT;

  return (
    <div className="source-strip">
      {visible.map((source, index) => (
        <a
          className="source-card"
          href={source.url}
          target="_blank"
          rel="noreferrer"
          key={`${source.url}-${index}`}
        >
          <span className="source-card-favicon">
            {faviconUrl(source.domain) ? (
              <img
                src={faviconUrl(source.domain)}
                alt=""
                width={16}
                height={16}
                onError={(event) => {
                  event.currentTarget.style.display = "none";
                }}
              />
            ) : (
              <Globe size={13} className="source-card-favicon-fallback" />
            )}
          </span>

          <span className="source-card-body">
            <strong>{source.title}</strong>
            <span>{source.domain}</span>
          </span>

          {source.verified && <span className="source-card-trust" title="Verified" />}
          <ExternalLink size={13} className="source-card-go" />
        </a>
      ))}

      {!showAll && remaining > 0 && (
        <button
          type="button"
          className="source-card source-card-more"
          onClick={() => setShowAll(true)}
        >
          +{remaining} more
        </button>
      )}
    </div>
  );
}
