'use client';

import { useState } from 'react';

export default function ResultsPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    try {
      const res = await fetch(`http://localhost:8000/response?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data.results || []);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <h1 className="text-2xl font-semibold">Search Documents</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
        className="border p-2 rounded w-80"
      />
      <button
        onClick={handleSearch}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Search
      </button>
      <div className="mt-4 w-full max-w-xl">
        {results.length > 0 ? (
          results.map((res, idx) => (
            <div key={idx} className="border p-3 rounded mb-2 bg-gray-50">
              {res.document || JSON.stringify(res)}
            </div>
          ))
        ) : (
          <p className="text-gray-500 mt-2">No results yet</p>
        )}
      </div>
    </div>
  );
}
