"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/",            label: "Home" },
  { href: "/courts",      label: "Find Courts" },
  { href: "/matchmaking", label: "Matchmaking" },
];

export default function Navbar() {
  const pathname = usePathname();
  return (
    <nav style={{
      background: "#fff",
      borderBottom: "1px solid #e4e9e6",
      position: "sticky", top: 0, zIndex: 50,
    }}>
      <div style={{
        maxWidth: 960, margin: "0 auto",
        padding: "0 24px", height: 56,
        display: "flex", alignItems: "center",
        justifyContent: "space-between",
      }}>
        <Link href="/" style={{ display: "flex", alignItems: "center", gap: 10, textDecoration: "none" }}>
          <div style={{
            width: 28, height: 28, borderRadius: 6,
            background: "#0F6E56",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <circle cx="7" cy="7" r="6" stroke="white" strokeWidth="1.5"/>
              <path d="M4 7h6M7 4v6" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
          </div>
          <span style={{ fontWeight: 600, fontSize: 15, color: "#0F6E56", letterSpacing: "-0.2px" }}>
            CourtFind
          </span>
        </Link>

        <div style={{ display: "flex", gap: 2 }}>
          {links.map((l) => {
            const active = pathname === l.href;
            return (
              <Link key={l.href} href={l.href} style={{
                padding: "6px 14px", borderRadius: 8,
                fontSize: 13, fontWeight: active ? 600 : 400,
                textDecoration: "none",
                color: active ? "#0F6E56" : "#666",
                background: active ? "#f0faf5" : "transparent",
                transition: "all 0.12s",
              }}>
                {l.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
