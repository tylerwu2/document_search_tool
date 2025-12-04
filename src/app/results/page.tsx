'use client';

import { useState } from 'react';

export default function ResultsPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<string[]>([]); // State is an array of strings
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResults([]);

    try {
      const res = await fetch(`http://localhost:8000/response?query=${encodeURIComponent(query)}`);

      if (!res.ok) {
        let errData;
        try {
          errData = await res.json();
        } catch{  
            throw new Error(errData.detail || 'An error occurred');
        }
        throw new Error(errData.detail || 'An error occurred');
      }
      const data = await res.json();

      if (!data || !data.results || !Array.isArray(data.results)) {
        throw new Error('Invalid response format from server');
      }
      
      // The backend now sends {"results": ["...answer..."]}
      setResults(data.results || []);
    } catch (err) {
      console.error(err); 
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <h1 className="text-2xl font-semibold">Search Documents</h1>
      <div className="flex w-full max-w-lg">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Enter your query..."
          className="border p-2 rounded-l w-full"
        />
        <button
          onClick={handleSearch}
          className="bg-green-600 text-white px-4 py-2 rounded-r hover:bg-green-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="mt-4 w-full max-w-xl">
        {loading && <p>Generating response...</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        
        {/* FIX 6: Display the single text response cleanly */}
        {results.length > 0 && (
          <div className="border p-4 rounded bg-gray-50 whitespace-pre-wrap">
            <h2 className="font-semibold mb-2">Response:</h2>
            {results[0]}
          </div>
        )}
      </div>
    </div>
  );
}