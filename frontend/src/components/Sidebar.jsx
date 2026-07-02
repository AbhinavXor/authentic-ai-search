import { useState } from "react";
import {
  HelpCircle,
  LogOut,
  MessageSquarePlus,
  MoreHorizontal,
  PanelLeft,
  Palette,
  Pencil,
  Pin,
  Settings,
  Trash2
} from "lucide-react";

export default function Sidebar({
  visible,
  groupedHistory,
  activeChatId,
  onOpenChat,
  onNewChat,
  onCollapse,
  onTogglePin,
  onRename,
  onDelete
}) {
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [renamingId, setRenamingId] = useState(null);
  const [renameValue, setRenameValue] = useState("");

  function startRename(event, chat) {
    event.stopPropagation();
    setRenamingId(chat.id);
    setRenameValue(chat.title);
  }

  function commitRename(chatId) {
    if (renameValue.trim()) onRename(chatId, renameValue);
    setRenamingId(null);
  }

  return (
    <aside className={visible ? "sidebar" : "sidebar sidebar-hidden"}>
      <div className="sidebar-top">
        <button
          className="icon-action sidebar-collapse"
          onClick={onCollapse}
          aria-label="Collapse sidebar"
        >
          <PanelLeft size={18} />
        </button>

        <button className="new-chat-button" onClick={onNewChat}>
          <MessageSquarePlus size={16} />
          New chat
        </button>
      </div>

      <div className="sidebar-section">
        {groupedHistory.length === 0 && (
          <>
            <p className="sidebar-label">Today</p>
            <p className="empty-history">No conversations yet</p>
          </>
        )}

        {groupedHistory.map((group) => (
          <div key={group.label}>
            <p className="sidebar-label">{group.label}</p>

            {group.items.map((chat) => (
              <div
                key={chat.id}
                className={
                  chat.id === activeChatId ? "history-item active" : "history-item"
                }
                onClick={() => onOpenChat(chat.id)}
              >
                {renamingId === chat.id ? (
                  <input
                    className="rename-input"
                    autoFocus
                    value={renameValue}
                    onClick={(e) => e.stopPropagation()}
                    onChange={(e) => setRenameValue(e.target.value)}
                    onBlur={() => commitRename(chat.id)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") commitRename(chat.id);
                      if (e.key === "Escape") setRenamingId(null);
                    }}
                  />
                ) : (
                  <span className="history-title">{chat.title}</span>
                )}

                <div className="history-actions">
                  <button
                    className={chat.pinned ? "history-action pinned" : "history-action"}
                    onClick={(e) => {
                      e.stopPropagation();
                      onTogglePin(chat.id);
                    }}
                    title={chat.pinned ? "Unpin" : "Pin"}
                  >
                    <Pin size={13} />
                  </button>
                  <button
                    className="history-action"
                    onClick={(e) => startRename(e, chat)}
                    title="Rename"
                  >
                    <Pencil size={13} />
                  </button>
                  <button
                    className="history-action danger"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(chat.id);
                    }}
                    title="Delete"
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className="sidebar-footer-wrapper">
        {showProfileMenu && (
          <div className="profile-menu">
            <div className="profile-menu-header">
              <div className="user-dot">A</div>
              <div className="profile-menu-identity">
                <strong>MR ABHINAV</strong>
                <span>abhinavankit21@gmail.com</span>
              </div>
            </div>

            <div className="profile-menu-divider" />

            <button>
              <Settings size={15} />
              Settings
            </button>
            <button>
              <Palette size={15} />
              Appearance
            </button>
            <button>
              <HelpCircle size={15} />
              Help &amp; support
            </button>

            <div className="profile-menu-divider" />

            <button
              className="profile-menu-danger"
              onClick={() => alert("Auth not wired up yet.")}
            >
              <LogOut size={15} />
              Log out
            </button>
          </div>
        )}

        <button
          className="sidebar-footer"
          onClick={() => setShowProfileMenu((open) => !open)}
        >
          <div className="user-dot">A</div>
          <span>Mr Abhinav</span>
          <MoreHorizontal size={16} className="profile-chevron" />
        </button>
      </div>
    </aside>
  );
}
