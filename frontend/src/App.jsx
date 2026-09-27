import React, { useState, useEffect } from 'react';
import {
  Brain,
  Building2,
  Plus,
  Sparkles,
  MessageSquareText,
  Calendar,
  Database,
  Briefcase
} from 'lucide-react';
import {
  fetchHealth,
  fetchDeals,
  createDeal,
  fetchInteractions,
  fetchMeetingBrief
} from './services/api';
import DealCard from './components/DealCard';
import MeetingBriefView from './components/MeetingBriefView';
import AskAgentChat from './components/AskAgentChat';
import TimelineView from './components/TimelineView';
import MemoryEvidenceView from './components/MemoryEvidenceView';
import AddInteractionModal from './components/AddInteractionModal';

export default function App() {
  const [deals, setDeals] = useState([]);
  const [selectedDeal, setSelectedDeal] = useState(null);
  const [activeTab, setActiveTab] = useState('brief');

  const [health, setHealth] = useState({ api: 'checking', hindsight: 'checking', llm: 'checking' });

  const [briefData, setBriefData] = useState(null);
  const [briefLoading, setBriefLoading] = useState(false);
  const [briefError, setBriefError] = useState(null);

  const [interactions, setInteractions] = useState([]);
  const [isInteractionModalOpen, setIsInteractionModalOpen] = useState(false);
  const [isAddDealModalOpen, setIsAddDealModalOpen] = useState(false);

  // Add deal form states
  const [newDealId, setNewDealId] = useState('');
  const [newDealName, setNewDealName] = useState('');
  const [newClientName, setNewClientName] = useState('');
  const [newStage, setNewStage] = useState('Discovery');
  const [newBudget, setNewBudget] = useState('₹100,000');
  const [newSummary, setNewSummary] = useState('');

  const checkStatus = async () => {
    const status = await fetchHealth();
    setHealth(status);
  };

  const loadDeals = async () => {
    try {
      const list = await fetchDeals();
      setDeals(list);
      if (list.length > 0 && !selectedDeal) {
        setSelectedDeal(list[0]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    checkStatus();
    loadDeals();
  }, []);

  const loadDealData = async (deal) => {
    if (!deal) return;

    try {
      const inters = await fetchInteractions(deal.id);
      setInteractions(inters);
    } catch (e) {
      console.error(e);
    }

    loadBrief(deal.id);
  };

  const loadBrief = async (dealId) => {
    setBriefLoading(true);
    setBriefError(null);
    try {
      const data = await fetchMeetingBrief(dealId);
      setBriefData(data);
    } catch (e) {
      setBriefError(e.message || 'Unable to generate brief from Hindsight memory');
      setBriefData(null);
    } finally {
      setBriefLoading(false);
    }
  };

  useEffect(() => {
    if (selectedDeal) {
      loadDealData(selectedDeal);
    }
  }, [selectedDeal]);

  const handleCreateDeal = async (e) => {
    e.preventDefault();
    if (!newDealName.trim()) return;
    const cleanId = newDealId || newDealName.toLowerCase().replace(/[^a-z0-9]/g, '-');
    try {
      const created = await createDeal({
        id: cleanId,
        name: newDealName,
        client_name: newClientName || newDealName,
        stage: newStage,
        budget: newBudget,
        summary: newSummary
      });
      await loadDeals();
      setSelectedDeal(created);
      setIsAddDealModalOpen(false);
      setNewDealName('');
      setNewClientName('');
      setNewSummary('');
    } catch (e) {
      alert(`Failed to create deal: ${e.message}`);
    }
  };

  const isHindsightConnected = health.hindsight === 'healthy';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Header Bar */}
      <header className="bg-slate-900/90 border-b border-slate-800/80 sticky top-0 z-40 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-tr from-blue-600 to-cyan-500 rounded-xl shadow-lg shadow-blue-500/20">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-slate-100 tracking-tight flex items-center gap-2">
                Deal Intelligence
                <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
                  Hindsight Agent
                </span>
              </h1>
              <p className="text-xs text-slate-400">
                Self-Improving Deal Memory & Strategic Sales Agent
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Real Health Indicator Badge */}
            <div className="hidden sm:flex items-center gap-2 text-xs bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
              <span
                className={`w-2 h-2 rounded-full ${
                  isHindsightConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'
                }`}
              ></span>
              <span className="text-slate-300 font-medium">Hindsight Memory Engine:</span>
              <span
                className={`font-semibold ${
                  isHindsightConnected ? 'text-emerald-400' : 'text-rose-400'
                }`}
              >
                {isHindsightConnected ? 'Connected' : 'Offline'}
              </span>
            </div>

            <button
              onClick={() => setIsAddDealModalOpen(true)}
              className="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-xs flex items-center gap-1.5 shadow-lg shadow-blue-500/20 transition-colors"
            >
              <Plus className="w-4 h-4" /> New Deal
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 py-6 flex-1 w-full grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Sidebar: Deal List */}
        <div className="lg:col-span-4 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Briefcase className="w-3.5 h-3.5 text-blue-400" /> Deals Portfolio ({deals.length})
            </h2>
          </div>

          <div className="space-y-3">
            {deals.map((deal) => (
              <DealCard
                key={deal.id}
                deal={deal}
                isSelected={selectedDeal?.id === deal.id}
                onSelect={(d) => setSelectedDeal(d)}
              />
            ))}
          </div>
        </div>

        {/* Right Main Panel: Selected Deal Workspace */}
        <div className="lg:col-span-8 space-y-5">
          {selectedDeal ? (
            <>
              {/* Deal Header Card */}
              <div className="p-6 bg-slate-900/80 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-3">
                    <h2 className="text-2xl font-bold text-slate-100">{selectedDeal.name}</h2>
                    <span className="text-xs px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30 font-medium">
                      {selectedDeal.stage}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Client: <span className="text-slate-200 font-medium">{selectedDeal.client_name}</span> • Memory Bank: <code className="text-blue-400">deal-{selectedDeal.id}</code>
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-[11px] text-slate-400 block uppercase tracking-wider">Target Value</span>
                    <span className="text-lg font-bold text-emerald-400">{selectedDeal.budget || 'N/A'}</span>
                  </div>
                  <button
                    onClick={() => setIsInteractionModalOpen(true)}
                    className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl text-xs flex items-center gap-2 transition-colors shadow-lg shadow-blue-500/20"
                  >
                    <Plus className="w-4 h-4" /> Add Interaction / Outcome
                  </button>
                </div>
              </div>

              {/* Navigation Tabs */}
              <div className="flex items-center gap-2 border-b border-slate-800/80 pb-1 text-xs font-semibold">
                {[
                  { id: 'brief', label: 'Meeting Brief', icon: Sparkles },
                  { id: 'chat', label: 'Ask Deal Agent', icon: MessageSquareText },
                  { id: 'timeline', label: 'Interactions & Outcomes', icon: Calendar },
                  { id: 'memories', label: 'Hindsight Memory Evidence', icon: Database }
                ].map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`px-4 py-2.5 rounded-lg flex items-center gap-2 transition-all ${
                        activeTab === tab.id
                          ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {tab.label}
                    </button>
                  );
                })}
              </div>

              {/* Tab Content Panels */}
              <div className="pt-2">
                {activeTab === 'brief' && (
                  <MeetingBriefView
                    briefData={briefData}
                    loading={briefLoading}
                    error={briefError}
                    onRefresh={() => loadBrief(selectedDeal.id)}
                  />
                )}

                {activeTab === 'chat' && (
                  <AskAgentChat
                    dealId={selectedDeal.id}
                    dealName={selectedDeal.name}
                  />
                )}

                {activeTab === 'timeline' && (
                  <TimelineView
                    dealId={selectedDeal.id}
                    interactions={interactions}
                    onAddClick={() => setIsInteractionModalOpen(true)}
                  />
                )}

                {activeTab === 'memories' && (
                  <MemoryEvidenceView dealId={selectedDeal.id} />
                )}
              </div>
            </>
          ) : (
            <div className="text-center p-12 bg-slate-900/40 rounded-2xl border border-slate-800 text-slate-400">
              Select a deal from the left sidebar to view its Hindsight Memory Workspace.
            </div>
          )}
        </div>
      </main>

      {/* Add Interaction Modal */}
      {selectedDeal && (
        <AddInteractionModal
          dealId={selectedDeal.id}
          isOpen={isInteractionModalOpen}
          onClose={() => setIsInteractionModalOpen(false)}
          onSuccess={() => loadDealData(selectedDeal)}
        />
      )}

      {/* New Deal Modal */}
      {isAddDealModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-slate-100 mb-1">Create New Sales Deal</h3>
            <p className="text-xs text-slate-400 mb-4">
              Initializes a dedicated Hindsight memory bank for this deal.
            </p>

            <form onSubmit={handleCreateDeal} className="space-y-3.5 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Deal Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Tesla Motors"
                  value={newDealName}
                  onChange={(e) => setNewDealName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Client Name</label>
                <input
                  type="text"
                  placeholder="e.g. Tesla Inc."
                  value={newClientName}
                  onChange={(e) => setNewClientName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Deal Stage</label>
                  <select
                    value={newStage}
                    onChange={(e) => setNewStage(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
                  >
                    <option value="Discovery">Discovery</option>
                    <option value="Evaluation">Evaluation</option>
                    <option value="Negotiation">Negotiation</option>
                    <option value="Closed Won">Closed Won</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Budget Target</label>
                  <input
                    type="text"
                    value={newBudget}
                    onChange={(e) => setNewBudget(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Summary / Objective</label>
                <textarea
                  rows="3"
                  placeholder="Brief deal objective..."
                  value={newSummary}
                  onChange={(e) => setNewSummary(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
                ></textarea>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsAddDealModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium"
                >
                  Create Deal Bank
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
