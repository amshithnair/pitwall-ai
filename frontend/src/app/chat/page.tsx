"use client";

import { useState } from 'react';
import { useAuthStore } from '@/store/useStore';
import Link from 'next/link';

export default function AIChat() {
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8007/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, session_id: 'session-123' })
      });
      const data = await res.json();
      setMessages([...newMessages, { role: 'ai', content: data.response }]);
    } catch (err) {
      setMessages([...newMessages, { role: 'ai', content: 'Error communicating with Orchestrator.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-300">
      <header className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900">
        <h1 className="text-xl font-bold text-white">AI Race Engineer</h1>
        <Link href="/" className="text-blue-400 hover:text-blue-300">Back to Dashboard</Link>
      </header>
      
      <main className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-4 rounded-xl ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-800 border border-slate-700'}`}>
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && <div className="text-slate-500 animate-pulse">AI is thinking...</div>}
      </main>

      <footer className="p-4 border-t border-slate-800 bg-slate-900">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about strategy, telemetry, or rules..."
            className="flex-1 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button type="submit" disabled={isLoading} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg disabled:opacity-50 transition-colors">
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}
