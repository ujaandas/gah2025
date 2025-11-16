import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { ThemeProvider } from "@/components/theme-provider";
import { HydrationHandler } from "@/components/HydrationHandler";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "FlowLens - AI Agent Testing Platform",
  description: "Test AI agents safely with visual graph editor, red-team testing, and real-time execution tracing"
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // Add loading class to prevent transitions during hydration
              document.documentElement.classList.add('loading');
            `,
          }}
        />
      </head>
      <body className={`${inter.variable} ${inter.className} antialiased loading`}>
        <HydrationHandler />
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange={false}
        >
          <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-1 flex flex-col w-full">
              {children}
            </main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
