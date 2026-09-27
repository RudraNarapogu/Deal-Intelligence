import React, { useState } from 'react';
import { X, Save, MessageSquare, CheckCircle, FileText } from 'lucide-react';
import { addInteraction } from '../services/api';

export default function AddInteractionModal({ dealId, isOpen, onClose, onSuccess }) {
  const [type, setType] = useState('meeting');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [title, setTitle] = useState('');
  const [transcript, setTranscript] = useState('');
  const [saving, setSaving] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!transcript.trim()) return;

    setSaving(true);
    try {
      await addInteraction(dealId, {
        type,
        date,
        title: title || `${type.toUpperCase()} on ${date}`,
        transcript,
        context: type === 'outcome' ? 'sales meeting outcome and learning' : 'sales meeting'
      });
      setTitle('');
      setTranscript('');
      onSuccess();
      onClose();
    } catch (err) {
      alert('Failed to record interaction');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-200"
        >
          <X className="w-5 h-5" />
        </button>

        <h3 className="text-lg font-bold text-slate-100 mb-1">
          Add Sales Meeting / Outcome
        </h3>
        <p className="text-xs text-slate-400 mb-5">
          Submitting will run Hindsight <code className="text-blue-400">retain()</code> to automatically extract facts, objections & learning signals.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Interaction Type</label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'meeting', label: 'Meeting', icon: MessageSquare },
                { id: 'outcome', label: 'Outcome / Learning', icon: CheckCircle },
                { id: 'email', label: 'Email / Note', icon: FileText }
              ].map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setType(item.id)}
                    className={`p-2.5 rounded-lg border font-medium flex items-center justify-center gap-1.5 transition-colors ${
                      type === item.id
                        ? 'bg-blue-600 text-white border-blue-500'
                        : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    {item.label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Date</label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-medium mb-1">Title (Optional)</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Technical Architecture Review"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">
              Transcript / Notes / Learning Outcome
            </label>
            <textarea
              rows="5"
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              placeholder="Paste raw transcript or notes. E.g. Client accepted our 10-day implementation plan. David Vance requested SOC2 security architecture whitepaper..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-slate-200 focus:outline-none focus:border-blue-500 leading-relaxed"
            ></textarea>
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving || !transcript.trim()}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg font-medium flex items-center gap-2 shadow-lg shadow-blue-500/10"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Retaining in Hindsight...' : 'Retain in Hindsight'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
