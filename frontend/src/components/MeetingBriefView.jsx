import React from 'react';
import { Sparkles, BrainCircuit, RefreshCw, CheckCircle2, ShieldAlert, Target } from 'lucide-react';

export default function MeetingBriefView({ briefData, loading, onRefresh }) {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-slate-900/40 rounded-xl border border-slate-800">
        <RefreshCw className="w-8 h-8 text-blue-400 animate-spin mb-3" />
        <p className="text-slate-300 font-medium">Recalling Hindsight deal memory & generating brief...</p>
        <p className="text-xs text-slate-500 mt-1">Analyzing facts, objections, entity graph & temporal momentum</p>
      </div>
    );
  }

  if (!briefData) {
    return (
      <div className="text-center p-8 bg-slate-900/40 rounded-xl border border-slate-800">
        <p className="text-slate-400">Click below to generate an Executive Meeting Brief for this deal.</p>
        <button
          onClick={onRefresh}
          className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-sm flex items-center gap-2 mx-auto"
        >
          <Sparkles className="w-4 h-4" /> Generate Meeting Brief
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-950/60 to-slate-900 border border-blue-800/40 rounded-xl">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
            <BrainCircuit className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
              Meeting Preparation Brief
            </h2>
            <p className="text-xs text-slate-400">
              Grounded strictly in retrieved Hindsight memory bank (<span className="text-blue-300">deal-{briefData.deal_id}</span>)
            </p>
          </div>
        </div>
        <button
          onClick={onRefresh}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5 text-blue-400" /> Refresh Brief
        </button>
      </div>

      {/* Main Brief Content */}
      <div className="p-6 bg-slate-900/80 rounded-xl border border-slate-800 text-slate-200 leading-relaxed text-sm whitespace-pre-wrap font-sans">
        {briefData.meeting_brief}
      </div>

      {/* Memory Evidence Inspector */}
      <div className="p-5 bg-slate-900/90 rounded-xl border border-blue-900/30">
        <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <h3 className="font-semibold text-slate-200 text-sm">
              Hindsight Memory Evidence ({briefData.evidence?.length || 0} Retrieved Items)
            </h3>
          </div>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
            Grounded RAG Proof
          </span>
        </div>

        {briefData.evidence && briefData.evidence.length > 0 ? (
          <div className="space-y-2.5">
            {briefData.evidence.map((item) => (
              <div
                key={item.id}
                className="p-3 bg-slate-950/60 rounded-lg border border-slate-800/80 flex items-start gap-3 text-xs"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                <div className="flex-1">
                  <p className="text-slate-200">{item.text}</p>
                  <div className="flex items-center gap-3 mt-1.5 text-[11px] text-slate-400">
                    <span className="text-blue-400 font-medium">{item.type}</span>
                    <span>•</span>
                    <span>{item.timestamp}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400 italic">No direct memory evidence items returned.</p>
        )}
      </div>
    </div>
  );
}
