import React from 'react';

export default function PostCard({ post }: { post: any }) {
  return (
    <div className="bg-card text-card-foreground p-6 rounded-lg shadow-sm border border-border mb-4">
      <div className="flex items-center mb-4">
        <div className="w-10 h-10 bg-muted rounded-full flex items-center justify-center mr-3 font-semibold text-muted-foreground">
          {post.author?.name?.charAt(0) || "U"}
        </div>
        <div>
          <h4 className="font-semibold">{post.author?.name || "Unknown User"}</h4>
          <p className="text-xs text-muted-foreground">@{post.author?.username || "unknown"}</p>
        </div>
      </div>
      <p className="mb-4 text-sm leading-relaxed">{post.content}</p>
      <div className="flex items-center gap-6 text-sm text-muted-foreground border-t border-border pt-4">
        <button className="flex items-center gap-2 hover:text-primary transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          Like
        </button>
        <button className="flex items-center gap-2 hover:text-primary transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/></svg>
          Comment
        </button>
        <button className="flex items-center gap-2 hover:text-primary transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>
          Save
        </button>
      </div>
    </div>
  );
}
