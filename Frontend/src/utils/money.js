export function eurToCents(input) {
    const s = String(input ?? "").trim().replace(",", ".");
    
    if (!s) return 0;

    if (!/^\d+(\.\d{0,2})?$/.test(s)) throw new Error("Invalid amount format");

    const [euros, frac = ""] = s.split(".");
    const cents = (frac + "00").slice(0, 2);
    return Number(euros) * 100 + Number(cents);
}

export function centsToEur(cents) {
    const num = Number(cents || 0);
    const euros = Math.floor(num / 100);
    const cen = String(num % 100).padStart(2, "0");
    return `${euros}.${cen}`;
}