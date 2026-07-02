import { useEffect, useRef, useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatHeader from "./components/ChatHeader";
import EmptyState from "./components/EmptyState";
import Composer from "./components/Composer";
import ThinkingTimeline from "./components/ThinkingTimeline";
import { UserMessage, AssistantMessage } from "./components/MessageList";

import { useChatController } from "./hooks/useChatController";

import "katex/dist/katex.min.css";
import "./App.css";

const SIDEBAR_STORAGE_KEY = "authenticai:sidebarOpen";

// First-time visitors get a closed sidebar. Once a person makes a choice,
// that choice sticks across reloads and never gets silently overridden by
// navigation (new chat, switching chats, sending a message, etc).
function getInitialSidebarState() {
  if (typeof window === "undefined") return false;
  try {
    return window.localStorage.getItem(SIDEBAR_STORAGE_KEY) === "true";
  } catch {
    return false;
  }
}

function App() {
  const [showSidebar, setShowSidebar] = useState(getInitialSidebarState);
  const bottomRef = useRef(null);

  const {
    activeChatId,
    activeMessages,
    activePending,
    groupedHistory,
    feedback,
    revealed,
    markRevealed,
    sendMessage,
    regenerate,
    stopGeneration,
    startNewChat,
    openChat,
    togglePin,
    renameChat,
    deleteChat,
    submitFeedback
  } = useChatController();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeMessages, activePending]);

  useEffect(() => {
    try {
      window.localStorage.setItem(SIDEBAR_STORAGE_KEY, String(showSidebar));
    } catch {
      // localStorage unavailable (private mode, etc) — state just won't persist
    }
  }, [showSidebar]);

  const isEmpty = activeMessages.length === 0 && !activePending;

  return (
    <div className="app-shell">
      <Sidebar
        visible={showSidebar}
        groupedHistory={groupedHistory}
        activeChatId={activeChatId}
        onOpenChat={openChat}
        onNewChat={startNewChat}
        onCollapse={() => setShowSidebar(false)}
        onTogglePin={togglePin}
        onRename={renameChat}
        onDelete={deleteChat}
      />

      <div className="chat-app">
        <ChatHeader
          sidebarVisible={showSidebar}
          onOpenSidebar={() => setShowSidebar(true)}
          onNewChat={startNewChat}
        />

        <main className="chat-main">
          <div className="messages">
            {isEmpty && <EmptyState />}

            {activeMessages.map((message, index) =>
              message.role === "user" ? (
                <UserMessage key={message.id} message={message} />
              ) : (
                <AssistantMessage
                  key={message.id}
                  message={message}
                  isLast={index === activeMessages.length - 1}
                  chatIsPending={Boolean(activePending)}
                  revealed={revealed}
                  markRevealed={markRevealed}
                  onRegenerate={(previousQuery) =>
                    regenerate(activeChatId, previousQuery)
                  }
                  onFeedback={submitFeedback}
                  feedbackStatus={feedback[message.id]}
                />
              )
            )}

            {activePending && (
              <ThinkingTimeline
                step={activePending.step}
                onStop={() => stopGeneration(activeChatId)}
              />
            )}

            <div ref={bottomRef} />
          </div>
        </main>

        <Composer
          sidebarVisible={showSidebar}
          isPending={Boolean(activePending)}
          onSend={sendMessage}
          onStop={() => stopGeneration(activeChatId)}
        />
      </div>
    </div>
  );
}

export default App;
