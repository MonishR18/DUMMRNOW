"use client";

import React, { useState } from 'react';

export default function CreatePost({ onPostCreated }: { onPostCreated: () => void }) {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      });
      if (res.ok) {
        setContent('');
        onPostCreated();
      }
    } catch (error) {
      console.error("Failed to create post", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-card text-card-foreground p-6 rounded-lg shadow-sm border border-border mb-6">
      <form onSubmit={handleSubmit}>
        <textarea
          className="w-full bg-background border border-input rounded-md p-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring resize-none mb-3"
          rows={3}
          placeholder="What's on your mind? Got a request?"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          disabled={loading}
        />
        <div className="flex justify-end">
          <button 
            type="submit" 
            disabled={loading || !content.trim()}
            className="bg-primary text-primary-foreground px-4 py-2 rounded-md text-sm font-medium hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            {loading ? "Posting..." : "Share Post"}
          </button>
        </div>
      </form>
    </div>
  );
}
