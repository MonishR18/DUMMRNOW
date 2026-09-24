"use client";

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function ExplorePage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/tasks');
        if (res.ok) {
          const data = await res.json();
          setTasks(data);
        }
      } catch (error) {
        console.error("Failed to fetch tasks", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  return (
    <div className="max-w-4xl mx-auto py-12 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Explore Requests</h1>
        <p className="text-muted-foreground">Find tasks to take up and build your reputation.</p>
      </div>

      {loading ? (
        <div className="text-center py-12 text-muted-foreground">Loading tasks...</div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">No open requests available.</div>
      ) : (
        <div className="grid gap-6">
          {tasks.map(task => (
            <div 
              key={task.id} 
              className="bg-card text-card-foreground p-6 rounded-lg shadow-sm border border-border cursor-pointer hover:border-primary transition-colors"
              onClick={() => router.push(`/tasks/${task.id}`)}
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold">{task.title}</h3>
                {task.budget && <span className="font-medium text-primary">₹{task.budget}</span>}
              </div>
              <p className="text-muted-foreground text-sm mb-4 line-clamp-2">{task.description}</p>
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                {task.category && <span className="bg-secondary text-secondary-foreground px-2 py-1 rounded-md">{task.category}</span>}
                <span>Posted by {task.creator?.name || "Unknown"}</span>
                <span>{new Date(task.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
