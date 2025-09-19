"use client";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen gap-6">
      <h1 className="text-3xl font-bold">Document Search Tool</h1>
      <div className="flex gap-4">
        <Link href="/upload" className="px-4 py-2 bg-blue-500 text-white rounded">
          Upload Document
        </Link>
        <Link href="/results" className="px-4 py-2 bg-green-500 text-white rounded">
          Search Responses
        </Link>
      </div>
    </main>
  );
}
