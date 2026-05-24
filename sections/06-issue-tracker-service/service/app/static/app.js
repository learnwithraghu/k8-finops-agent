const boardEl = document.getElementById('board');
const refreshBtn = document.getElementById('refreshBtn');
const issueDrawerEl = document.getElementById('issueDrawer');
const closeDrawerBtn = document.getElementById('closeDrawerBtn');
const selectedLabelEl = document.getElementById('selectedLabel');
const selectedIssueEl = document.getElementById('selectedIssue');
const updateForm = document.getElementById('updateForm');

const columns = [
  ['backlog', 'Backlog'],
  ['todo', 'To do'],
  ['in_progress', 'In progress'],
  ['done', 'Done'],
];

let currentIssues = [];
let selectedIssue = null;
let draggingIssueId = null;

function chip(text, cls = '') {
  return `<span class="chip ${cls}">${text}</span>`;
}

function renderCard(issue) {
  return `
    <article class="issue-card" draggable="true" data-id="${issue.id}">
      <div class="issue-card-top">
        <span class="issue-key">${issue.key}</span>
        ${chip(issue.priority, `priority-${issue.priority}`)}
      </div>
      <h4>${issue.title}</h4>
      <div class="issue-subtitle">${issue.namespace || 'default'} · ${issue.resource_kind || 'resource'}${issue.assignee ? ` · ${issue.assignee}` : ''}</div>
      <div class="issue-meta">
        ${chip(`$${Number(issue.cost_impact || 0).toFixed(2)}/mo`)}
        ${chip(issue.suggested_owner || 'no owner')}
      </div>
    </article>
  `;
}

function renderBoard(items) {
  boardEl.innerHTML = columns.map(([key, label]) => {
    const columnItems = items.filter(issue => issue.status === key);
    const cards = columnItems.map(renderCard).join('');

    return `
      <section class="column column-${key}" data-status="${key}">
        <div class="column-head">
          <h3>${label}</h3>
          <span class="column-badge">${columnItems.length}</span>
        </div>
        <div class="column-body">${cards || '<div class="detail-empty">Drop cards here</div>'}</div>
      </section>
    `;
  }).join('');

  boardEl.querySelectorAll('.issue-card').forEach(card => {
    card.addEventListener('click', () => openIssue(Number(card.dataset.id)));
    card.addEventListener('dragstart', onDragStart);
    card.addEventListener('dragend', onDragEnd);
  });

  boardEl.querySelectorAll('.column').forEach(column => {
    column.addEventListener('dragover', onDragOver);
    column.addEventListener('dragleave', onDragLeave);
    column.addEventListener('drop', onDrop);
  });
}

function openDrawer() {
  issueDrawerEl.classList.remove('hidden');
  issueDrawerEl.setAttribute('aria-hidden', 'false');
}

function closeDrawer() {
  issueDrawerEl.classList.add('hidden');
  issueDrawerEl.setAttribute('aria-hidden', 'true');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

function renderMarkdown(text) {
  if (!text) return '';
  let html = escapeHtml(text);

  html = html.replace(/^### (.+)$/gm, '<h4 class="jira-h4">$1</h4>');
  html = html.replace(/^## (.+)$/gm, '<h3 class="jira-h3">$1</h3>');

  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/`([^`]+)`/g, '<code class="jira-code">$1</code>');

  html = html.replace(/^- (.+)$/gm, '<li class="jira-li">$1</li>');
  html = html.replace(/^\d+\. (.+)$/gm, '<li class="jira-li">$1</li>');

  html = html.replace(/(<li class="jira-li">.*?<\/li>(\s|$))+/gs, (match) => {
    return '<ul class="jira-list">' + match + '</ul>';
  });

  html = html.replace(/^-{3,}$/gm, '<hr class="jira-hr" />');

  html = html.replace(/\n\n/g, '</p><p class="jira-p">');
  html = html.replace(/\n/g, '<br />');

  html = '<p class="jira-p">' + html + '</p>';

  html = html.replace(/<p class="jira-p"><\/p>/g, '');

  const listRE = /(<ul class="jira-list">(?:\s|.)*?<\/ul>)/g;
  html = html.replace(listRE, (match) => {
    const cleaned = match
      .replace(/<br \/>/g, '')
      .replace(/<\/p><p class="jira-p">/g, '');
    return cleaned;
  });

  return html;
}

function renderIssueDetails(issue) {
  if (!issue) {
    selectedLabelEl.textContent = 'Select a ticket';
    selectedIssueEl.innerHTML = '<div class="detail-empty">Click a card to open it.</div>';
    updateForm.classList.add('hidden');
    closeDrawer();
    return;
  }

  openDrawer();
  selectedLabelEl.textContent = `${issue.key}`;

  const costStr = `$${Number(issue.cost_impact || 0).toFixed(2)}/mo`;
  const labels = (issue.labels && issue.labels.length) ? issue.labels : [];

  selectedIssueEl.innerHTML = `
    <div class="jira-ticket">
      <div class="jira-badges">
        <span class="jira-status status-${issue.status}">${issue.status.replace('_', ' ')}</span>
        ${chip(issue.priority, `priority-${issue.priority}`)}
        ${chip(costStr)}
      </div>

      <h2 class="jira-title">${issue.title}</h2>

      <div class="jira-body">
        <div class="jira-description">
          <div class="jira-section-label">Description</div>
          <div class="jira-description-body">${renderMarkdown(issue.body || issue.summary || '—')}</div>
        </div>

        <aside class="jira-sidebar">
          <div class="jira-field-group">
            <div class="jira-field">
              <span class="jira-field-label">Status</span>
              <span class="jira-field-value">${issue.status.replace('_', ' ')}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Priority</span>
              <span class="jira-field-value">${issue.priority}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Assignee</span>
              <span class="jira-field-value">${issue.assignee || 'Unassigned'}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Suggested Owner</span>
              <span class="jira-field-value">${issue.suggested_owner || '—'}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Cost Center</span>
              <span class="jira-field-value">${issue.suggested_cost_center || '—'}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Category</span>
              <span class="jira-field-value">${issue.category || '—'}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Namespace</span>
              <span class="jira-field-value">${issue.namespace || '—'}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Resource</span>
              <span class="jira-field-value">${issue.resource_kind || '—'} / ${issue.resource_name || '—'}</span>
            </div>
            <div class="jira-field">
              <span class="jira-field-label">Source</span>
              <span class="jira-field-value">${issue.source || '—'}</span>
            </div>
          </div>
        </aside>
      </div>

      ${labels.length ? `
      <div class="jira-labels-section">
        <span class="jira-section-label">Labels</span>
        <div class="jira-labels">${labels.map(l => `<span class="jira-label">${escapeHtml(l)}</span>`).join('')}</div>
      </div>` : ''}
    </div>
  `;

  updateForm.classList.remove('hidden');
  updateForm.elements.id.value = issue.id;
  updateForm.elements.status.value = issue.status;
  updateForm.elements.assignee.value = issue.assignee || '';
}

async function loadIssues(preserveSelection = true) {
  const res = await fetch('/api/issues');
  const data = await res.json();
  currentIssues = data.items;
  renderBoard(currentIssues);

  if (preserveSelection && selectedIssue) {
    const fresh = currentIssues.find(issue => issue.id === selectedIssue.id);
    selectedIssue = fresh || null;
  }

  renderIssueDetails(selectedIssue);
}

async function openIssue(id) {
  const res = await fetch(`/issue/${id}`);
  selectedIssue = await res.json();
  renderIssueDetails(selectedIssue);
}

async function patchIssue(id, payload) {
  const res = await fetch(`/issue/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  const updated = await res.json();
  selectedIssue = updated;
  await loadIssues();
  renderIssueDetails(updated);
}

function onDragStart(event) {
  draggingIssueId = Number(event.currentTarget.dataset.id);
  event.currentTarget.classList.add('dragging');
  event.dataTransfer.effectAllowed = 'move';
  event.dataTransfer.setData('text/plain', String(draggingIssueId));
}

function onDragEnd(event) {
  event.currentTarget.classList.remove('dragging');
  draggingIssueId = null;
  boardEl.querySelectorAll('.column').forEach(column => column.classList.remove('drop-target'));
}

function onDragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = 'move';
  event.currentTarget.classList.add('drop-target');
}

function onDragLeave(event) {
  event.currentTarget.classList.remove('drop-target');
}

async function onDrop(event) {
  event.preventDefault();
  const column = event.currentTarget;
  column.classList.remove('drop-target');

  const issueId = Number(event.dataTransfer.getData('text/plain') || draggingIssueId);
  const status = column.dataset.status;
  const issue = currentIssues.find(item => item.id === issueId);

  if (!issue || issue.status === status) {
    return;
  }

  await patchIssue(issueId, {
    status,
    assignee: issue.assignee || '',
  });
}

updateForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = Number(updateForm.elements.id.value);
  await patchIssue(id, {
    status: updateForm.elements.status.value,
    assignee: updateForm.elements.assignee.value,
  });
});

refreshBtn.addEventListener('click', () => loadIssues(false));
closeDrawerBtn.addEventListener('click', () => {
  selectedIssue = null;
  renderIssueDetails(null);
});
loadIssues();
