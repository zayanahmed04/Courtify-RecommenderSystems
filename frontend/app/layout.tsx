import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "CourtFind",
  description: "Sports court discovery and player matchmaking for Karachi",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main style={{ maxWidth: 960, margin: "0 auto", padding: "32px 24px" }}>
          {children}
        </main>
      </body>
    </html>
  );
}
