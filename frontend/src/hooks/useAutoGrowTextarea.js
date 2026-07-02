import { useEffect } from "react";

export function useAutoGrowTextarea(ref, value, maxHeight = 180) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, maxHeight) + "px";
  }, [ref, value, maxHeight]);
}
