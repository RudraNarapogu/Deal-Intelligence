import React, { useState } from 'react';
import { Send, Bot, User, Sparkles, CheckCircle2, AlertTriangle } from 'lucide-react';
import { askAgent } from '../services/api';

export default function AskAgentChat({ dealId, dealName }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hello! I am your Deal Intelligence Agent for **${dealName}**. Ask me any question about customer requirements, objections, pricing, stakeholders, or past approach outcomes.`,
      evidence: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sampleQuestions = [
    `What are ${dealName}'s current objections?`,
    `What pricing and budget details were discussed for ${dealName}?`,
    `What should I emphasize in tomorrow's ${dealName} meeting?`
  ];

  const handleSend = async (questionText) => {
    const query = questionText || input;
    if (!query.trim() || loading) return;

    const userMsg = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await askAgent(dealId, query);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.answer,
          evidence: res.evidence || []
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `⚠️ Error: ${err.message || 'Unable to query Deal Agent.'}`,
          evidence: [],
          isError: true
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-slate-900/60 rounded-xl border border-slate-800 overflow-hidden">
      {/* Sample Quick Questions */}
      <div className="p-3 bg-slate-950/80 border-b border-slate-800/80 flex items-center gap-2 overflow-x-auto text-xs">
        <span className="text-slate-400 shrink-0 font-medium flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" /> Quick Prompts:
        </span>
        {sampleQuestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            disabled={loading}
            className="px-2.5 py-1 bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border border-slate-700/60 rounded-full shrink-0 transition-colors"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Messages List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${
              msg.role === 'user' ? 'flex-row-reverse' : ''
            }`}
          >
            <div
              className={`p-2 rounded-lg text-white shrink-0 ${
                msg.role === 'user'
                  ? 'bg-blue-600'
                  : msg.isError
                  ? 'bg-rose-900/80 border border-rose-700'
                  : 'bg-slate-800 border border-slate-700'
              }`}
            >
              {msg.role === 'user' ? (
                <User className="w-4 h-4" />
              ) : msg.isError ? (
                <AlertTriangle className="w-4 h-4 text-rose-400" />
              ) : (
                <Bot className="w-4 h-4 text-blue-400" />
              )}
            </div>

            <div
              className={`max-w-[80%] rounded-xl p-4 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600/90 text-white font-medium'
                  : msg.isError
                  ? 'bg-rose-950/80 text-rose-200 border border-rose-800'
                  : 'bg-slate-800/90 text-slate-200 border border-slate-700/70'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>

              {/* Memory Evidence Footer if present */}
              {msg.evidence && msg.evidence.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-700/60 space-y-2">
                  <span className="text-[11px] font-semibold text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Retrieved Hindsight Memory Facts:
                  </span>
                  <div className="space-y-1.5">
                    {msg.evidence.slice(0, 3).map((item) => (
                      <div
                        key={item.id}
                        className="p-2 bg-slate-950/70 rounded border border-slate-800 text-[11px] text-slate-300"
                      >
                        {item.text}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-slate-800 border border-slate-700">
              <Bot className="w-4 h-4 text-blue-400 animate-pulse" />
            </div>
            <div className="bg-slate-800/60 text-slate-400 text-xs px-4 py-2 rounded-xl border border-slate-700/50">
              Recalling Hindsight memories and reasoning with LLM...
            </div>
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="p-3 bg-slate-950 border-t border-slate-800 flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={`Ask Deal Agent about ${dealName}...`}
          className="flex-1 bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-lg px-4 py-2.5 focus:outline-none focus:border-blue-500"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !input.trim()}
          className="p-2.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
