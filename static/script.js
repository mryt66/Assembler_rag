const chatEl = document.getElementById('chat');
const formEl = document.getElementById('chat-form');
const msgEl = document.getElementById('message');
const statusEl = document.getElementById('status');

let history = [];

function addMessage(role, content) {
  const wrapper = document.createElement('div');
  wrapper.className = `message ${role}`;
  wrapper.innerHTML = `
    <div class="avatar">${role === 'user' ? '🧑' : '🤖'}</div>
    <div>
      <div class="role">${role === 'user' ? 'You' : 'Assistant'}</div>
      <div class="content">${escapeHtml(content)}</div>
    </div>
  `;
  chatEl.appendChild(wrapper);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function addSystem(text) {
  const sys = document.createElement('div');
  sys.className = 'system';
  sys.textContent = text;
  chatEl.appendChild(sys);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function sendMessage(text) {
  statusEl.textContent = 'Thinking...';
  formEl.querySelector('button').disabled = true;
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: text, history })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }
    const data = await res.json();
    addMessage('assistant', data.response);
    if (data.trace_id) {
      addSystem(`trace: ${data.trace_id}`);
    }
    history.push({ role: 'assistant', message: data.response });
  } catch (e) {
    addMessage('assistant', `Error: ${e.message}`);
  } finally {
    statusEl.textContent = 'Ready';
    formEl.querySelector('button').disabled = false;
  }
}

formEl.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = msgEl.value.trim();
  if (!text) return;
  addMessage('user', text);
  history.push({ role: 'user', message: text });
  msgEl.value = '';
  sendMessage(text);
});

// Warmup health check
fetch('/health').then(() => {
  const sys = document.createElement('div');
  sys.className = 'system';
  sys.textContent = 'Connected. Ask me anything about your knowledge base.';
  chatEl.appendChild(sys);
});
