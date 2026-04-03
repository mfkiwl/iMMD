'use client';

import { useState } from 'react';

export default function ChatBox() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    const res = await fetch('http://localhost:5005/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input }),
    });

    const data = await res.json();

    const agentMessage = { role: 'agent', content: data.reply };
    setMessages((prev) => [...prev, agentMessage]);

    setInput('');
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="h-[400px] overflow-y-scroll border p-4 bg-gray-50 space-y-3 rounded">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`p-2 rounded ${
              m.role === 'user' ? 'bg-blue-100' : 'bg-green-100'
            }`}
          >
            <strong>{m.role === 'user' ? 'You' : 'Agent'}:</strong> {m.content}
          </div>
        ))}
      </div>

      <div className="mt-4 flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
