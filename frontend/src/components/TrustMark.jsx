import { CheckCircle2 } from "lucide-react";

/**
 * Deliberately says nothing. No "Verified" / "Partially Verified" /
 * "Unverified" labels, no warning colors. A quiet check if the answer
 * cleared verification (fully or partially), nothing at all if it didn't.
 */
export default function TrustMark({ status }) {
  const normalized = String(status || "").toLowerCase();
  const isVerified = normalized === "verified" || normalized === "partially_verified";

  if (!isVerified) return null;

  return (
    <span className="trust-mark" tabIndex={0}>
      <CheckCircle2 size={15} strokeWidth={2.3} />
      <span className="trust-tooltip">Checked against sources</span>
    </span>
  );
}
