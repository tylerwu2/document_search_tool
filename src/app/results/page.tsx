'use client';

import { useState } from 'react';

export default function ResultsPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResults([]);

    try {
      // Create AbortController for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 90000); // 90 second timeout

      const res = await fetch(
        `http://localhost:8000/response?query=${encodeURIComponent(query)}`,
        { signal: controller.signal }
      );

      clearTimeout(timeoutId);

      if (!res.ok) {
        let errData;
        try {
          errData = await res.json();
        } catch {  
          throw new Error('An error occurred');
        }
        throw new Error(errData.detail || 'An error occurred');
      }
      const data = await res.json();

      if (!data || !data.results || !Array.isArray(data.results)) {
        throw new Error('Invalid response format from server');
      }
      
      setResults(data.results || []);
    } catch (err: any) {
      console.error(err); 
      if (err.name === 'AbortError') {
        setError('Request timed out. The model may be taking too long to respond.');
      } else {
        setError((err as Error).message);
      }
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
        {loading && <p>Generating response... (this may take 10-30 seconds)</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        
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