import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'Document Search Tool',
  description: 'Upload documents and ask questions for summaries',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        {/* Navbar */}
        <header className="bg-blue-600 text-white p-4 shadow-md">
          <nav className="flex justify-center gap-6">
            <Link href="/" className="hover:underline">
              Home
            </Link>
            <Link href="/upload" className="hover:underline">
              Upload
            </Link>
            <Link href="/results" className="hover:underline">
              Search
            </Link>
          </nav>
        </header>

        {/* Main content */}
        <main className="p-8">{children}</main>
      </body>
    </html>
  );
}
