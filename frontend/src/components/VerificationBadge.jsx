function VerificationBadge({ badge, status }) {
  const className = `verification-badge ${status || "unknown"}`;

  return (
    <span className={className}>
      {badge || "❌ Unverified"}
    </span>
  );
}

export default VerificationBadge;