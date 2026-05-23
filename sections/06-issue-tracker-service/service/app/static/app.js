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

function renderIssueDetails(issue) {
  if (!issue) {
    selectedLabelEl.textContent = 'Select a ticket';
    selectedIssueEl.innerHTML = '<div class="detail-empty">Click a card to open it.</div>';
    updateForm.classList.add('hidden');
    closeDrawer();
    return;
  }

  openDrawer();
  selectedLabelEl.textContent = `${issue.key} • ${issue.status}`;
  selectedIssueEl.innerHTML = `
    <div class="detail-view">
      <div class="detail-row"><strong>Title</strong><span>${issue.title}</span></div>
      <div class="detail-row"><strong>Summary</strong><span>${issue.summary || '-'}</span></div>
      <div class="detail-row"><strong>Body</strong><span>${issue.body || '-'}</span></div>
      <div class="detail-row"><strong>Namespace</strong><span>${issue.namespace || '-'}</span></div>
      <div class="detail-row"><strong>Resource</strong><span>${issue.resource_kind || '-'} / ${issue.resource_name || '-'}</span></div>
      <div class="detail-row"><strong>Priority</strong><span>${issue.priority}</span></div>
      <div class="detail-row"><strong>Owner</strong><span>${issue.suggested_owner || '-'}</span></div>
      <div class="detail-row"><strong>Assignee</strong><span>${issue.assignee || '-'}</span></div>
      <div class="detail-row"><strong>Reasoning</strong><span>${issue.reasoning || '-'}</span></div>
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
