import type { Metadata } from "next";
import { Geist, Geist_Mono, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-sans",
  subsets: ["latin"],
  weight: ["300"],
});

export const metadata: Metadata = {
  title: "Gah2025",
  description: "Great Agent Hack 2025"
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${ibmPlexMono.variable} ${ibmPlexMono.className} antialiased`}
        style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: '#ffffff',
        }}
      >
        <Navbar />
        <main
          style={{
            flex: 1,
            minHeight: 0,
            display: 'flex',
            flexDirection: 'column',
            width: '100%',
          }}
        >
          {children}
        </main>
      </body>
    </html>
  );
}
