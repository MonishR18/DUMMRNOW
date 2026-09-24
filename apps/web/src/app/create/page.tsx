"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function CreateRequestPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    budget: '',
    deadline: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        ...formData,
        budget: formData.budget ? parseFloat(formData.budget) : null,
        deadline: formData.deadline ? new Date(formData.deadline).toISOString() : null
      };
      
      const res = await fetch('http://localhost:8000/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      
      if (res.ok) {
        const data = await res.json();
        router.push(`/tasks/${data.id}`);
      }
    } catch (error) {
      console.error("Failed to create request", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-8">Post a Request</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">Title</label>
          <input 
            type="text" 
            required 
            placeholder="e.g., Build a React portfolio"
            className="w-full border border-input rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-primary"
            value={formData.title}
            onChange={e => setFormData({...formData, title: e.target.value})}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">Description</label>
          <textarea 
            required 
            rows={5}
            placeholder="Describe what you need..."
            className="w-full border border-input rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-primary"
            value={formData.description}
            onChange={e => setFormData({...formData, description: e.target.value})}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Category (Optional)</label>
            <input 
              type="text" 
              placeholder="e.g., Web Development"
              className="w-full border border-input rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-primary"
              value={formData.category}
              onChange={e => setFormData({...formData, category: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Budget (Optional, ₹)</label>
            <input 
              type="number" 
              placeholder="e.g., 5000"
              className="w-full border border-input rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-primary"
              value={formData.budget}
              onChange={e => setFormData({...formData, budget: e.target.value})}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Deadline (Optional)</label>
          <input 
            type="date" 
            className="w-full border border-input rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-primary"
            value={formData.deadline}
            onChange={e => setFormData({...formData, deadline: e.target.value})}
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-primary text-primary-foreground py-3 rounded-md font-medium hover:bg-primary/90 transition-colors"
        >
          {loading ? "Posting..." : "Post Request"}
        </button>
      </form>
    </div>
  );
}
