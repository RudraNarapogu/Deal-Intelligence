const API_BASE = 'http://localhost:8000/api';

export async function fetchDeals() {
  const res = await fetch(`${API_BASE}/deals`);
  if (!res.ok) throw new Error('Failed to fetch deals');
  return res.json();
}

export async function createDeal(dealData) {
  const res = await fetch(`${API_BASE}/deals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dealData)
  });
  if (!res.ok) throw new Error('Failed to create deal');
  return res.json();
}

export async function fetchInteractions(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/interactions`);
  if (!res.ok) throw new Error('Failed to fetch interactions');
  return res.json();
}

export async function addInteraction(dealId, payload) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/interactions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to record interaction');
  return res.json();
}

export async function fetchMeetingBrief(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/meeting-brief`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) throw new Error('Failed to generate meeting brief');
  return res.json();
}

export async function askAgent(dealId, question) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  if (!res.ok) throw new Error('Failed to query agent');
  return res.json();
}

export async function fetchDealMemories(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/memories`);
  if (!res.ok) throw new Error('Failed to fetch memories');
  return res.json();
}
