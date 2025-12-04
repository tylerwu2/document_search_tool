'use client';

import { useState } from 'react';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setStatus('');

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      

      let data;
      try {
        data = await res.json();
      } catch (jsonError) {
        // If response is not JSON, use status text as error message
        throw new Error(`Server error: ${res.status} ${res.statusText}`);
      }
      
      if (res.ok) {
        setStatus(data.status || 'Upload successful');
      } else {
        setStatus(data.error || 'Upload failed');
      }
    } catch (error) {
      console.error(error);
      setStatus('Upload failed: ' + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <h1 className="text-2xl font-semibold">Upload Document</h1>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="border p-2 rounded"
      />  
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? 'Uploading...' : 'Upload'}
      </button>
      {status && <p className="text-gray-700">{status}</p>}
    </div>
  );
}
