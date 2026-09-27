const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const parseErrorMessage = async (res, defaultMsg) => {
  try {
    const data = await res.json();
    if (data.detail) {
      if (typeof data.detail === 'string') return data.detail;
      if (Array.isArray(data.detail)) {
        return data.detail.map((e) => (typeof e === 'object' ? e.msg || JSON.stringify(e) : String(e))).join(', ');
      }
      return JSON.stringify(data.detail);
    }
    return typeof data === 'string' ? data : JSON.stringify(data);
  } catch (e) {
    return defaultMsg;
  }
};

export async function fetchHealth() {
  try {
    const healthUrl = API_BASE.endsWith('/api')
      ? `${API_BASE}/health`
      : `${API_BASE}/api/health`;

    const res = await fetch(healthUrl);
    if (!res.ok) return { api: 'unhealthy', hindsight: 'unhealthy', llm: 'unhealthy' };
    return res.json();
  } catch (e) {
    return { api: 'unhealthy', hindsight: 'unhealthy', llm: 'unhealthy' };
  }
}

export async function fetchDeals() {
  const res = await fetch(`${API_BASE}/deals`);
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to fetch deals');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function createDeal(dealData) {
  const res = await fetch(`${API_BASE}/deals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dealData)
  });
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to create deal');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function fetchInteractions(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/interactions`);
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to fetch interactions');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function addInteraction(dealId, payload) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/interactions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to record interaction');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function recordOutcome(dealId, outcomeData) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/outcomes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(outcomeData)
  });
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to record outcome');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function fetchOutcomes(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/outcomes`);
  if (!res.ok) return [];
  return res.json();
}

export async function fetchMeetingBrief(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/meeting-brief`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to generate meeting brief');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function askAgent(dealId, question) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to query agent');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function fetchDealMemories(dealId) {
  const res = await fetch(`${API_BASE}/deals/${dealId}/memories`);
  if (!res.ok) {
    const errMsg = await parseErrorMessage(res, 'Failed to fetch memories');
    throw new Error(errMsg);
  }
  return res.json();
}
