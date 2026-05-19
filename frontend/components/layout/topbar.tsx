"use client";
import { ThemeToggle } from "@/components/theme-toggle";
import Link from "next/link";

export function Topbar() {
  return (
    <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b bg-card/80 backdrop-blur px-4 md:px-6">
      <div className="flex items-center gap-3">
        <Link href="/" className="md:hidden font-bold">
          Resume<span className="text-primary">AI</span>
        </Link>
        <span className="hidden md:block text-sm text-muted-foreground">
          AI-powered Resume Screening &amp; ATS Scoring
        </span>
      </div>
      <div className="flex items-center gap-2">
        <ThemeToggle />
      </div>
    </header>
  );
}
