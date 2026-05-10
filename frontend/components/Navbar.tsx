"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Home" },
  { href: "/courts", label: "Court Search" },
  { href: "/matchmaking", label: "Matchmaking" },
  { href: "/how-it-works", label: "How It Works" },
];

export default function Navbar() {
  const pathname = usePathname();
  return (
    <nav style={{
      background: "#fff",
      borderBottom: "1px solid #e8ede9",
      position: "sticky",
      top: 0,
      zIndex: 50,
    }}>
      <div style={{
        maxWidth: 896,
        margin: "0 auto",
        padding: "0 1rem",
        height: 56,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}>
        <Link href="/" style={{ display: "flex", alignItems: "center", gap: 8, textDecoration: "none" }}>
          <div style={{
            width: 30, height: 30, borderRadius: 8,
            background: "linear-gradient(135deg, #0F6E56, #1D9E75)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 600 }}>C</span>
          </div>
          <span style={{ fontWeight: 600, fontSize: 15, color: "#0F6E56" }}>CourtFind AI</span>
        </Link>
        <div style={{ display: "flex", gap: 4 }}>
          {links.map((l) => (
            <Link key={l.href} href={l.href} style={{
              padding: "6px 12px",
              borderRadius: 8,
              fontSize: 13,
              fontWeight: 500,
              textDecoration: "none",
              color: pathname === l.href ? "#0F6E56" : "#555",
              background: pathname === l.href ? "#E1F5EE" : "transparent",
              transition: "all 0.15s",
            }}>
              {l.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
