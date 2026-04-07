// CodeBuddy — Main JS

document.addEventListener('DOMContentLoaded', () => {
  initDropdowns();
  initModals();
  initAlerts();
  initSkillTags();
  initChatAutoScroll();
  initAvatarColors();
  initNavActive();
});

// ── DROPDOWNS ─────────────────────────────────────
function initDropdowns() {
  document.querySelectorAll('[data-dropdown]').forEach(trigger => {
    const menuId = trigger.getAttribute('data-dropdown');
    const menu = document.getElementById(menuId);
    if (!menu) return;
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.classList.toggle('open');
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
  });
}

// ── MODALS ────────────────────────────────────────
function initModals() {
  document.querySelectorAll('[data-modal-open]').forEach(btn => {
    const id = btn.getAttribute('data-modal-open');
    const modal = document.getElementById(id);
    if (!modal) return;
    btn.addEventListener('click', () => modal.classList.add('open'));
  });
  document.querySelectorAll('[data-modal-close], .modal-overlay').forEach(el => {
    el.addEventListener('click', (e) => {
      if (e.target === el || el.hasAttribute('data-modal-close')) {
        el.closest('.modal-overlay')?.classList.remove('open');
        if (el.hasAttribute('data-modal-close')) {
          document.getElementById(el.getAttribute('data-modal-close'))?.classList.remove('open');
        }
      }
    });
  });
  document.querySelectorAll('.modal').forEach(m => {
    m.addEventListener('click', e => e.stopPropagation());
  });
}

// ── ALERTS AUTO-DISMISS ───────────────────────────
function initAlerts() {
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(alert => {
    const delay = parseInt(alert.getAttribute('data-auto-dismiss')) || 4000;
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      alert.style.transition = 'all 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, delay);
  });
}

// ── SKILL TAGS INPUT ──────────────────────────────
function initSkillTags() {
  document.querySelectorAll('[data-skill-input]').forEach(container => {
    const input = container.querySelector('input[type="text"]');
    const hiddenInput = container.querySelector('input[type="hidden"]');
    const tagList = container.querySelector('.tag-list');
    if (!input || !hiddenInput) return;

    let skills = hiddenInput.value ? hiddenInput.value.split(',').filter(Boolean) : [];

    function render() {
      tagList.innerHTML = skills.map((s, i) =>
        `<span class="skill-tag">${s} <button type="button" onclick="removeSkill(${i})" style="background:none;border:none;color:inherit;cursor:pointer;margin-left:4px;font-size:0.85em">×</button></span>`
      ).join('');
      hiddenInput.value = skills.join(',');
    }

    window.removeSkill = (i) => { skills.splice(i, 1); render(); };

    input.addEventListener('keydown', (e) => {
      if ((e.key === 'Enter' || e.key === ',') && input.value.trim()) {
        e.preventDefault();
        skills.push(input.value.trim().replace(/,/g, ''));
        input.value = '';
        render();
      }
    });
    render();
  });
}

// ── CHAT AUTO SCROLL ──────────────────────────────
function initChatAutoScroll() {
  const chatMsgs = document.querySelector('.chat-messages');
  if (chatMsgs) {
    chatMsgs.scrollTop = chatMsgs.scrollHeight;
    // Poll for new messages every 5s (simple long-polling alternative)
    if (window.chatPollUrl) {
      setInterval(() => {
        fetch(window.chatPollUrl)
          .then(r => r.json())
          .then(data => {
            if (data.html) {
              chatMsgs.innerHTML = data.html;
              chatMsgs.scrollTop = chatMsgs.scrollHeight;
            }
          }).catch(() => {});
      }, 5000);
    }
  }
}

// ── AVATAR COLOR FROM NAME ────────────────────────
function initAvatarColors() {
  document.querySelectorAll('[data-avatar-name]').forEach(el => {
    const name = el.getAttribute('data-avatar-name') || '';
    const colors = ['#6366f1','#8b5cf6','#ec4899','#f59e0b','#10b981','#3b82f6','#ef4444','#06b6d4'];
    let hash = 0;
    for (const c of name) hash = (hash << 5) - hash + c.charCodeAt(0);
    el.style.background = colors[Math.abs(hash) % colors.length];
  });
}

// ── NAV ACTIVE STATE ──────────────────────────────
function initNavActive() {
  const path = window.location.pathname;
  document.querySelectorAll('.navbar-nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href && path.startsWith(href) && href !== '/') {
      a.classList.add('active');
    } else if (href === '/' && path === '/') {
      a.classList.add('active');
    }
  });
}

// ── COPY TO CLIPBOARD ─────────────────────────────
function copyToClipboard(text) {
  navigator.clipboard?.writeText(text).then(() => {
    showToast('Copied!', 'success');
  }).catch(() => {});
}

// ── TOAST NOTIFICATION ────────────────────────────
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `alert alert-${type}`;
  toast.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;min-width:240px;animation:fadeSlideUp 0.3s ease';
  toast.setAttribute('data-auto-dismiss', '3000');
  toast.textContent = message;
  document.body.appendChild(toast);
  initAlerts();
}

// ── CONFIRM DELETE ────────────────────────────────
function confirmAction(message, formId) {
  if (confirm(message)) {
    document.getElementById(formId)?.submit();
  }
}

// ── TASK STATUS UPDATE ────────────────────────────
function updateTaskStatus(formId, status) {
  const form = document.getElementById(formId);
  if (form) {
    form.querySelector('[name="status"]').value = status;
    form.submit();
  }
}

// ── DIFFICULTY FILTER ─────────────────────────────
function filterProjects(difficulty) {
  const url = new URL(window.location);
  if (difficulty) {
    url.searchParams.set('difficulty', difficulty);
  } else {
    url.searchParams.delete('difficulty');
  }
  window.location = url.toString();
}
