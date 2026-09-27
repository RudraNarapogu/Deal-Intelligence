import React from 'react';
import { Calendar, Plus, MessageSquare, CheckCircle, FileText, ArrowUpRight } from 'lucide-react';

export default function TimelineView({ interactions, onAddClick }) {
  const getIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'outcome':
        return <CheckCircle className="w-4 h-4 text-emerald-400" />;
      case 'email':
        return <FileText className="w-4 h-4 text-purple-400" />;
      default:
        return <MessageSquare className="w-4 h-4 text-blue-400" />;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between p-4 bg-slate-900/60 rounded-xl border border-slate-800">
        <div>
          <h3 className="font-semibold text-slate-100 text-base">Deal Interaction Timeline</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Every interaction is processed and retained into Hindsight long-term deal memory.
          </p>
        </div>
        <button
          onClick={onAddClick}
          className="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-xs flex items-center gap-2 transition-colors shadow-lg shadow-blue-500/10"
        >
          <Plus className="w-4 h-4" /> Add Meeting Transcript
        </button>
      </div>

      {interactions && interactions.length > 0 ? (
        <div className="relative border-l-2 border-slate-800 ml-4 pl-6 space-y-6">
          {interactions.map((item) => (
            <div key={item.id} className="relative group">
              {/* Dot */}
              <div className="absolute -left-[31px] top-1 p-1.5 bg-slate-900 rounded-full border border-slate-700 shadow">
                {getIcon(item.type)}
              </div>

              <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 group-hover:border-slate-700 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-200 text-sm">{item.title || item.type}</span>
                    <span className="text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 uppercase tracking-wider">
                      {item.type}
                    </span>
                  </div>
                  <span className="text-xs text-slate-400 flex items-center gap-1 font-medium">
                    <Calendar className="w-3.5 h-3.5 text-slate-500" />
                    {item.date}
                  </span>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap bg-slate-950/50 p-3 rounded-lg border border-slate-800/80 mt-2">
                  {item.transcript}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center p-8 bg-slate-900/40 rounded-xl border border-slate-800 text-slate-400 text-sm">
          No interactions recorded yet. Click 'Add Meeting Transcript' above to seed memories into Hindsight!
        </div>
      )}
    </div>
  );
}
