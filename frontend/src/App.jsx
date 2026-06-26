import { useState } from "react";

import VerificationBadge from "./components/VerificationBadge";
import EvidencePanel from "./components/EvidencePanel";
import ClaimLineagePanel from "./components/ClaimLineagePanel";
import CitationsPanel from "./components/CitationsPanel";

import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [feedbackStatus, setFeedbackStatus] = useState("");
  const [showDetails, setShowDetails] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const API_BASE_URL = "http://127.0.0.1:8000";

  function toggleSidebar() {
    setShowSidebar(!showSidebar);
  }

  function startNewChat() {
    setQuery("");
    setMessages([]);
    setActiveChatId(null);
    setFeedbackStatus("");
    setShowDetails(false);
  }

  function openHistoryItem(chat) {
    setActiveChatId(chat.id);
    setMessages(chat.messages);
    setQuery(chat.query);
    setFeedbackStatus("");
    setShowDetails(false);
  }

  function logout() {
    alert("Logout will be connected after auth is added.");
  }

  async function handleSearch(event) {
    event.preventDefault();

    if (!query.trim()) {
      return;
    }

    const cleanQuery = query.trim();

    const userMessage = {
      role: "user",
      content: cleanQuery
    };

    setMessages([userMessage]);
    setLoading(true);
    setFeedbackStatus("");
    setShowDetails(false);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: cleanQuery
        })
      });

      const data = await response.json();

      const assistantMessage = {
        role: "assistant",
        data: data
      };

      const newMessages = [userMessage, assistantMessage];
      const chatId = Date.now();

      setMessages(newMessages);
      setActiveChatId(chatId);

      setHistory((previous) => [
        {
          id: chatId,
          title:
            cleanQuery.length > 34
              ? `${cleanQuery.slice(0, 34)}...`
              : cleanQuery,
          query: cleanQuery,
          messages: newMessages
        },
        ...previous
      ]);
    } catch (error) {
      setMessages([
        userMessage,
        {
          role: "assistant",
          data: {
            answer: "Unable to connect to VRA backend.",
            verification_badge: "❌ Backend Error",
            verification_status: "unverified",
            warning_message: String(error),
            citations: []
          }
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function submitFeedback(feedbackType, result) {
    if (!result) {
      return;
    }

    const firstCitation =
      result.citations && result.citations.length > 0
        ? result.citations[0]
        : null;

    try {
      const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: query,
          answer: result.answer,
          feedback_type: feedbackType,
          source_domain: firstCitation ? firstCitation.domain : null,
          source_name: firstCitation ? firstCitation.source : null
        })
      });

      const data = await response.json();

      if (data.status === "success") {
        setFeedbackStatus("Feedback saved.");
      } else {
        setFeedbackStatus("Feedback could not be saved.");
      }
    } catch (error) {
      setFeedbackStatus("Feedback error: " + String(error));
    }
  }

  function LogoMark() {
    return (
      <div className="brand-logo" aria-label="Authentic AI logo">
        <div className="brand-logo-inner">A</div>
      </div>
    );
  }

  function renderSourceChips(result) {
    if (!result?.citations || result.citations.length === 0) {
      return null;
    }

    return (
      <div className="source-chips">
        {result.citations.map((source, index) => (
          <a
            key={`${source.domain}-${index}`}
            className="source-chip"
            href={source.url}
            target="_blank"
            rel="noreferrer"
          >
            <span className="source-icon">🌐</span>
            <span>
              <strong>{source.source}</strong>
              <small>{source.domain}</small>
            </span>
          </a>
        ))}
      </div>
    );
  }

  function renderAssistantMessage(result) {
    return (
      <div className="message assistant-message">
        <div className="avatar ai-avatar">
          <LogoMark />
        </div>

        <div className="message-content">
          {renderSourceChips(result)}

          <p className="assistant-answer">{result.answer}</p>

          {result.warning_message && (
            <div className="soft-warning">
              {result.warning_message}
            </div>
          )}

          <div className="verification-row">
            <VerificationBadge
              badge={result.verification_badge}
              status={result.verification_status}
            />

            <button
              className="details-toggle"
              onClick={() => setShowDetails(!showDetails)}
            >
              {showDetails
                ? "Hide verification details"
                : "View verification details"}
            </button>
          </div>

          {showDetails && (
            <div className="details-panel">
              <div className="metrics-grid">
                <div className="metric-card">
                  <span>Trust</span>
                  <strong>{result.trust_score}</strong>
                </div>

                <div className="metric-card">
                  <span>Quality</span>
                  <strong>
                    {result.answer_quality_score} /{" "}
                    {result.answer_quality_level}
                  </strong>
                </div>

                <div className="metric-card">
                  <span>Safety</span>
                  <strong>
                    {result.safety_score} / {result.safety_level}
                  </strong>
                </div>

                <div className="metric-card">
                  <span>Risk</span>
                  <strong>
                    {result.hallucination_risk_score} /{" "}
                    {result.hallucination_risk_level}
                  </strong>
                </div>
              </div>

              <div className="details-summary">
                <p>{result.verification_summary}</p>
                <p>
                  Sources: {result.verified_source_count} verified /{" "}
                  {result.failed_source_count} failed
                </p>
                <p>Consensus: {result.consensus_status}</p>
              </div>

              <div className="ranked-box">
                <h3>Ranked Sources</h3>

                {result.ranked_sources?.length > 0 ? (
                  <ol>
                    {result.ranked_sources.map((source) => (
                      <li key={`${source.domain}-${source.source_rank}`}>
                        <strong>#{source.source_rank}</strong> {source.source}
                        <br />
                        <span>
                          {source.domain} · Score {source.source_score}
                        </span>
                      </li>
                    ))}
                  </ol>
                ) : (
                  <p>No ranked sources available.</p>
                )}
              </div>

              <CitationsPanel citations={result.citations} />
              <EvidencePanel evidence={result.evidence_summary} />
              <ClaimLineagePanel lineage={result.claim_lineage} />

              <div className="feedback-box">
                <h3>Was this answer helpful?</h3>

                <div className="feedback-actions">
                  <button onClick={() => submitFeedback("upvote", result)}>
                    👍 Helpful
                  </button>

                  <button onClick={() => submitFeedback("downvote", result)}>
                    👎 Not Helpful
                  </button>

                  <button onClick={() => submitFeedback("report", result)}>
                    🚩 Report
                  </button>
                </div>

                {feedbackStatus && (
                  <p className="feedback-status">{feedbackStatus}</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside
        className={
          showSidebar
            ? "sidebar"
            : "sidebar sidebar-hidden"
        }
      >
        <div className="sidebar-top">
          <button className="new-chat-button" onClick={startNewChat}>
            ✦ New chat
          </button>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">Recents</p>

          {history.length === 0 && (
            <p className="empty-history">No recent chats yet</p>
          )}

          {history.map((chat) => (
            <button
              key={chat.id}
              className={
                chat.id === activeChatId
                  ? "history-item active"
                  : "history-item"
              }
              onClick={() => openHistoryItem(chat)}
            >
              {chat.title}
            </button>
          ))}
        </div>

        <div className="sidebar-footer-wrapper">
          {showProfileMenu && (
            <div className="profile-menu">
              <button>Settings</button>
              <button>Upgrade plan</button>
              <button onClick={logout}>Log out</button>
            </div>
          )}

          <button
            className="sidebar-footer"
            onClick={() => setShowProfileMenu(!showProfileMenu)}
          >
            <div className="user-dot">A</div>
            <span>MR ABHINAV</span>
            <span className="profile-chevron">⌄</span>
          </button>
        </div>
      </aside>

      <div className="chat-app">
        <header className="chat-header">
          <button
            className="menu-toggle"
            onClick={toggleSidebar}
            aria-label="Toggle sidebar"
          >
            ☰
          </button>

          <div className="brand-block">
            <LogoMark />

            <div>
              <h1>Authentic AI</h1>
              <p>Verified answers with trusted sources</p>
            </div>
          </div>
        </header>

        <main className="chat-main">
          <div className="messages">
            {messages.length === 0 && (
              <div className="empty-state">
                <LogoMark />
                <h2>What can I verify for you?</h2>
                <p>
                  Ask a question and get a sourced answer with verification
                  details.
                </p>
              </div>
            )}

            {messages.map((message, index) => {
              if (message.role === "user") {
                return (
                  <div className="message user-message" key={index}>
                    <div className="avatar user-avatar">You</div>

                    <div className="message-content">
                      {message.content}
                    </div>
                  </div>
                );
              }

              return (
                <div key={index}>
                  {renderAssistantMessage(message.data)}
                </div>
              );
            })}

            {loading && (
              <div className="message assistant-message">
                <div className="avatar ai-avatar">
                  <LogoMark />
                </div>

                <div className="message-content muted">
                  Verifying answer from trusted sources...
                </div>
              </div>
            )}
          </div>
        </main>

        <form
          className={
            showSidebar
              ? "chat-input-bar sidebar-open"
              : "chat-input-bar sidebar-closed"
          }
          onSubmit={handleSearch}
        >
          <input
            type="text"
            placeholder="Message Authentic AI..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />

          <button type="submit" disabled={loading}>
            {loading ? "..." : "➤"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;