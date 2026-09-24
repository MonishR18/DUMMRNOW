"use client";

import React, { useEffect, useState } from 'react';
import PostCard from '@/components/feed/PostCard';
import CreatePost from '@/components/feed/CreatePost';

export default function FeedPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('For You');

  const fetchFeed = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/feed');
      if (res.ok) {
        const data = await res.json();
        setPosts(data);
      }
    } catch (error) {
      console.error("Failed to fetch feed", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
  }, [activeTab]);

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 tracking-tight">Feed</h1>
        <p className="text-muted-foreground">See it. Take it up. Build it. Earn it.</p>
      </div>

      <div className="flex gap-6 border-b border-border mb-6">
        {['For You', 'Following', 'Campus', 'Trending'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-medium transition-colors relative ${
              activeTab === tab 
                ? 'text-foreground' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            {tab}
            {activeTab === tab && (
              <span className="absolute bottom-0 left-0 w-full h-0.5 bg-primary rounded-t-full" />
            )}
          </button>
        ))}
      </div>

      <CreatePost onPostCreated={fetchFeed} />

      {loading ? (
        <div className="text-center py-12 text-muted-foreground">Loading feed...</div>
      ) : posts.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          No posts yet. Be the first to share something!
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map(post => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}
    </div>
  );
}
