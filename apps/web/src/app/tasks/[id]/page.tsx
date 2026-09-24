"use client";

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

export default function TaskDetailPage() {
  const { id } = useParams();
  const [task, setTask] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showApplyModal, setShowApplyModal] = useState(false);
  const [applyMessage, setApplyMessage] = useState('');
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState(false);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/tasks/${id}`);
        if (res.ok) {
          const data = await res.json();
          setTask(data);
          // For mockup: check if current mocked user (ID:1) has already applied
          if (data.applications?.some((app: any) => app.worker_id === 1)) {
            setApplied(true);
          }
        }
      } catch (error) {
        console.error("Failed to fetch task", error);
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchTask();
  }, [id]);

  const handleApply = async () => {
    setApplying(true);
    try {
      const res = await fetch(`http://localhost:8000/api/tasks/${id}/take-up`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: applyMessage }),
      });
      if (res.ok) {
        setApplied(true);
        setShowApplyModal(false);
      } else {
        const err = await res.json();
        alert(`Error: ${err.detail}`);
      }
    } catch (error) {
      console.error("Failed to apply", error);
    } finally {
      setApplying(false);
    }
  };

  if (loading) return <div className="text-center py-24 text-muted-foreground">Loading task...</div>;
  if (!task) return <div className="text-center py-24 text-muted-foreground">Task not found</div>;

  return (
    <div className="max-w-4xl mx-auto py-12 px-4 relative">
      <div className="bg-card text-card-foreground p-8 rounded-xl shadow-sm border border-border">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">{task.title}</h1>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span>Posted by {task.creator?.name || "Unknown"}</span>
              <span>•</span>
              <span>{new Date(task.created_at).toLocaleDateString()}</span>
            </div>
          </div>
          {task.budget && (
            <div className="text-2xl font-bold text-primary">₹{task.budget}</div>
          )}
        </div>

        <div className="mb-8">
          <h3 className="font-semibold mb-2">Description</h3>
          <p className="whitespace-pre-wrap leading-relaxed text-muted-foreground">{task.description}</p>
        </div>

        <div className="flex items-center justify-between border-t border-border pt-6 mt-6">
          <div className="flex gap-4">
            {task.category && (
              <span className="bg-secondary text-secondary-foreground px-3 py-1 rounded-md text-sm">{task.category}</span>
            )}
            <span className="bg-muted text-muted-foreground px-3 py-1 rounded-md text-sm">{task.status}</span>
          </div>
          
          <button 
            onClick={() => setShowApplyModal(true)}
            disabled={applied || task.status !== "OPEN"}
            className="bg-primary text-primary-foreground px-8 py-3 rounded-md font-bold hover:bg-primary/90 disabled:opacity-50 transition-colors shadow-sm"
          >
            {applied ? "ALREADY APPLIED" : task.status !== "OPEN" ? "NOT OPEN" : "TAKE IT UP"}
          </button>
        </div>
      </div>

      {showApplyModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-card text-card-foreground p-6 rounded-lg shadow-lg max-w-md w-full border border-border">
            <h2 className="text-xl font-bold mb-4">Why are you a good fit?</h2>
            <textarea 
              rows={4}
              placeholder="Tell the client why they should pick you..."
              className="w-full border border-input rounded-md p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-primary"
              value={applyMessage}
              onChange={e => setApplyMessage(e.target.value)}
            />
            <div className="flex justify-end gap-3">
              <button 
                onClick={() => setShowApplyModal(false)}
                className="px-4 py-2 rounded-md hover:bg-secondary transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={handleApply}
                disabled={applying}
                className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium hover:bg-primary/90 transition-colors"
              >
                {applying ? "Applying..." : "Submit Application"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
