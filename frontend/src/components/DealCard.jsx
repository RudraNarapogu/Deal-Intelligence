import React from 'react';
import { Building2, DollarSign, Calendar, ArrowRight } from 'lucide-react';

export default function DealCard({ deal, isSelected, onSelect }) {
  const getStageColor = (stage) => {
    switch (stage?.toLowerCase()) {
      case 'evaluation':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'negotiation':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'closed won':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      default:
        return 'bg-slate-700/50 text-slate-300 border-slate-600';
    }
  };

  return (
    <div
      onClick={() => onSelect(deal)}
      className={`p-5 rounded-xl border transition-all cursor-pointer ${
        isSelected
          ? 'bg-slate-800/90 border-blue-500 shadow-lg shadow-blue-500/10 ring-1 ring-blue-500/30'
          : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-800/50'
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-lg text-slate-100 flex items-center gap-2">
            <Building2 className="w-4 h-4 text-blue-400" />
            {deal.name}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">{deal.client_name}</p>
        </div>
        <span
          className={`text-xs px-2.5 py-1 rounded-full border font-medium ${getStageColor(
            deal.stage
          )}`}
        >
          {deal.stage}
        </span>
      </div>

      <p className="text-sm text-slate-300 line-clamp-2 mb-4">
        {deal.summary || 'Enterprise deal processing'}
      </p>

      <div className="flex items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-800/80">
        <div className="flex items-center gap-1 text-slate-200 font-medium">
          <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
          <span>{deal.budget || 'N/A'}</span>
        </div>
        <span className="flex items-center gap-1 text-blue-400 font-medium group-hover:translate-x-1 transition-transform">
          Open Workspace <ArrowRight className="w-3.5 h-3.5" />
        </span>
      </div>
    </div>
  );
}
