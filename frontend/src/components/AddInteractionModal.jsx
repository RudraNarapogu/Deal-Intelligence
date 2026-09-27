import React, { useState } from 'react';
import { X, Save, MessageSquare, CheckCircle, FileText, TrendingUp, AlertTriangle } from 'lucide-react';
import { addInteraction, recordOutcome } from '../services/api';

export default function AddInteractionModal({ dealId, isOpen, onClose, onSuccess }) {
  const [activeTab, setActiveTab] = useState('interaction'); // 'interaction' or 'outcome'

  // Interaction Form State
  const [type, setType] = useState('meeting');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [title, setTitle] = useState('');
  const [transcript, setTranscript] = useState('');

  // Outcome Form State
  const [actionTaken, setActionTaken] = useState('');
  const [result, setResult] = useState('');
  const [impact, setImpact] = useState('positive');
  const [notes, setNotes] = useState('');

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmitInteraction = async (e) => {
    e.preventDefault();
    if (!transcript.trim()) return;

    setSaving(true);
    setError('');
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
      setError(err.message || 'Failed to record interaction');
    } finally {
      setSaving(false);
    }
  };

  const handleSubmitOutcome = async (e) => {
    e.preventDefault();
    if (!actionTaken.trim() || !result.trim()) return;

    setSaving(true);
    setError('');
    try {
      await recordOutcome(dealId, {
        action_taken: actionTaken,
        result,
        impact,
        notes
      });
      setActionTaken('');
      setResult('');
      setNotes('');
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to record outcome learning');
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

        {/* Modal Tab Toggle */}
        <div className="flex items-center gap-2 mb-4 border-b border-slate-800 pb-3">
          <button
            type="button"
            onClick={() => { setActiveTab('interaction'); setError(''); }}
            className={`px-3 py-1.5 rounded-lg font-medium text-xs flex items-center gap-1.5 transition-colors ${
              activeTab === 'interaction'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" /> Add Interaction
          </button>
          <button
            type="button"
            onClick={() => { setActiveTab('outcome'); setError(''); }}
            className={`px-3 py-1.5 rounded-lg font-medium text-xs flex items-center gap-1.5 transition-colors ${
              activeTab === 'outcome'
                ? 'bg-emerald-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" /> Record Outcome & Learning
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-rose-950/80 border border-rose-800 rounded-lg text-rose-200 text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {/* Interaction Form */}
        {activeTab === 'interaction' ? (
          <form onSubmit={handleSubmitInteraction} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Interaction Type</label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: 'meeting', label: 'Meeting', icon: MessageSquare },
                  { id: 'call', label: 'Call', icon: FileText },
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
                  required
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
                  placeholder="e.g. Technical Security Review"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">
                Transcript / Notes (Min 5 chars)
              </label>
              <textarea
                rows="5"
                required
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                placeholder="Paste raw transcript or notes. E.g. Client requested 10-day implementation guarantee and SOC2 security whitepaper..."
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
                disabled={saving || transcript.trim().length < 5}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg font-medium flex items-center gap-2 shadow-lg shadow-blue-500/10"
              >
                <Save className="w-4 h-4" />
                {saving ? 'Retaining in Hindsight...' : 'Retain in Hindsight'}
              </button>
            </div>
          </form>
        ) : (
          /* Outcome & Learning Form */
          <form onSubmit={handleSubmitOutcome} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Sales Action Taken</label>
              <input
                type="text"
                required
                value={actionTaken}
                onChange={(e) => setActionTaken(e.target.value)}
                placeholder="e.g. Presented 10-day implementation deployment plan"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Customer Result / Reaction</label>
              <input
                type="text"
                required
                value={result}
                onChange={(e) => setResult(e.target.value)}
                placeholder="e.g. Client accepted implementation timeline with enthusiasm"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Impact Rating</label>
              <select
                value={impact}
                onChange={(e) => setImpact(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-emerald-500"
              >
                <option value="positive">Positive (Approach Succeeded)</option>
                <option value="negative">Negative (Approach Failed / Rejected)</option>
                <option value="neutral">Neutral (Unresolved / Information Only)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Strategic Learnings / Notes</label>
              <textarea
                rows="3"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. Demonstrating timeline proof resolved implementation fear. Security objection remains open for David Vance."
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-slate-200 focus:outline-none focus:border-emerald-500 leading-relaxed"
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
                disabled={saving || !actionTaken.trim() || !result.trim()}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded-lg font-medium flex items-center gap-2 shadow-lg shadow-emerald-500/10"
              >
                <Save className="w-4 h-4" />
                {saving ? 'Retaining Outcome...' : 'Retain Outcome & Learn'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
