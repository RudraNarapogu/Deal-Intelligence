import React, { useState, useEffect } from 'react';
import { Database, BrainCircuit, ShieldCheck, RefreshCw } from 'lucide-react';
import { fetchDealMemories } from '../services/api';

export default function MemoryEvidenceView({ dealId }) {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadMemories = async () => {
    setLoading(true);
    try {
      const data = await fetchDealMemories(dealId);
      setMemories(data.memories || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (dealId) loadMemories();
  }, [dealId]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between p-4 bg-slate-900/60 rounded-xl border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
            <Database className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 text-base">Hindsight Bank Memory Inspector</h3>
            <p className="text-xs text-slate-400">
              Live inspection of extracted facts, temporal notes, and entity relationships in bank <span className="text-purple-300">deal-{dealId}</span>
            </p>
          </div>
        </div>
        <button
          onClick={loadMemories}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium flex items-center gap-1.5"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-purple-400 ${loading ? 'animate-spin' : ''}`} /> Sync Memory
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-xs">Syncing with Hindsight Bank...</div>
      ) : memories.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {memories.map((mem, idx) => (
            <div
              key={idx}
              className="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 hover:border-purple-900/50 transition-colors text-xs space-y-2"
            >
              <div className="flex items-center justify-between text-slate-400">
                <span className="font-semibold text-purple-400 uppercase tracking-wider text-[10px] bg-purple-950/80 px-2 py-0.5 rounded border border-purple-800/50">
                  {mem.type || 'Memory Fact'}
                </span>
                <span>{mem.timestamp || 'Retained'}</span>
              </div>
              <p className="text-slate-200 leading-relaxed">{mem.text}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-8 text-center text-slate-400 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
          No memory units stored yet.
        </div>
      )}
    </div>
  );
}
