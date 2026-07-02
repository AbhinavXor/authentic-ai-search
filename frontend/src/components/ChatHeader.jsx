import { MessageSquarePlus, PanelLeft } from "lucide-react";
import { Wordmark } from "./Logo";

export default function ChatHeader({ sidebarVisible, onOpenSidebar, onNewChat }) {
  return (
    <header className="chat-header">
      {!sidebarVisible && (
        <>
          <button
            className="menu-toggle"
            onClick={onOpenSidebar}
            aria-label="Open sidebar"
          >
            <PanelLeft size={19} />
          </button>

          <button
            className="menu-toggle"
            onClick={onNewChat}
            aria-label="New chat"
          >
            <MessageSquarePlus size={18} />
          </button>
        </>
      )}

      <Wordmark />
    </header>
  );
}
