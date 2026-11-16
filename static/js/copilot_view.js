/**
 * Generative AI Copilot & Strategic Recommendations Controller
 */

window.CopilotView = {
    history: [],

    init() {
        this.loadRecommendations();
        this.initChat();
        this.initQuickPrompts();
        this.initRefreshButton();
    },

    initRefreshButton() {
        const btn = document.getElementById('btn-refresh-recs');
        if (btn) {
            btn.onclick = () => {
                btn.innerHTML = `<span class="pulse-dot"></span> Generating Strategy...`;
                this.loadRecommendations().finally(() => {
                    btn.innerHTML = `
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                        Regenerate AI Strategy
                    `;
                });
            };
        }
    },

    async loadRecommendations() {
        const grid = document.getElementById('recs-grid');
        if (!grid) return;

        try {
            const res = await fetch('/api/ai/recommendations');
            const data = await res.json();
            if (data.success && data.recommendations) {
                this.renderRecommendations(data.recommendations);
            }
        } catch (e) {
            console.error('Failed to load AI recommendations:', e);
        }
    },

    renderRecommendations(recs) {
        const grid = document.getElementById('recs-grid');
        if (!grid) return;

        grid.innerHTML = recs.map(r => {
            const impactPills = Object.entries(r.projected_impact || {}).map(([k, v]) => `
                <span><strong>${v}</strong> <small class="text-muted">(${k.replace(/_/g, ' ')})</small></span>
            `).join(' &bull; ');

            return `
                <div class="rec-card" style="border-left-color: ${r.color || '#3B82F6'};">
                    <div class="rec-card-top">
                        <span class="rec-category" style="color: ${r.color || '#3B82F6'};">${r.category}</span>
                        <span class="badge ${r.priority === 'CRITICAL' ? 'badge-danger' : (r.priority === 'HIGH' ? 'badge-warning' : 'badge-info')}">
                            ${r.badge || r.priority}
                        </span>
                    </div>
                    <h3 class="rec-card-title">${r.title}</h3>
                    <p class="rec-summary">${r.summary}</p>
                    <ul class="rec-steps">
                        ${(r.actionable_steps || []).map(s => `<li>${s}</li>`).join('')}
                    </ul>
                    <div class="rec-impact-row">
                        <span>🎯 Projected Impact:</span>
                        <div>${impactPills}</div>
                    </div>
                </div>
            `;
        }).join('');
    },

    initChat() {
        const form = document.getElementById('chat-form');
        const input = document.getElementById('chat-input');
        if (!form || !input) return;

        form.onsubmit = async (e) => {
            e.preventDefault();
            const text = input.value.trim();
            if (!text) return;

            input.value = '';
            this.appendMessage('user', text);

            // Show typing indicator
            const typingBubble = this.appendTypingBubble();

            try {
                const res = await fetch('/api/ai/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: text,
                        history: this.history
                    })
                });
                const data = await res.json();
                typingBubble.remove();

                if (data.success) {
                    this.appendMessage('copilot', data.reply, data.action_suggestion);
                    this.history.push({ role: 'user', content: text });
                    this.history.push({ role: 'assistant', content: data.reply });
                } else {
                    this.appendMessage('copilot', 'Apologies, I encountered an error while synthesizing telemetry.');
                }
            } catch (err) {
                typingBubble.remove();
                this.appendMessage('copilot', 'Network communication issue with Copilot service.');
            }
        };
    },

    initQuickPrompts() {
        document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
            btn.onclick = () => {
                const prompt = btn.dataset.prompt;
                const input = document.getElementById('chat-input');
                if (input) {
                    input.value = prompt;
                    document.getElementById('chat-form').dispatchEvent(new Event('submit'));
                }
            };
        });
    },

    appendMessage(role, text, action) {
        const chatBox = document.getElementById('chat-messages');
        if (!chatBox) return null;

        const bubble = document.createElement('div');
        bubble.className = `chat-bubble ${role === 'user' ? 'user-msg' : 'copilot-msg'}`;

        const senderLabel = role === 'user' ? 'You' : 'EcoTwin Copilot • Agent';

        // Markdown parsing
        let formattedText = this.formatMarkdown(text);

        let actionHtml = '';
        if (action && action.type === 'DISPATCH_TRUCK') {
            actionHtml = `
                <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--border-bright);">
                    <button class="btn btn-xs btn-primary" onclick="TwinView.dispatchSpecificTruck('${action.truck_id}')">
                        ⚡ ${action.label}
                    </button>
                </div>
            `;
        }

        bubble.innerHTML = `
            <div class="bubble-sender">${senderLabel}</div>
            <div class="bubble-content">${formattedText}</div>
            ${actionHtml}
        `;

        chatBox.appendChild(bubble);
        chatBox.scrollTop = chatBox.scrollHeight;
        return bubble;
    },

    appendTypingBubble() {
        const chatBox = document.getElementById('chat-messages');
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble copilot-msg';
        bubble.innerHTML = `
            <div class="bubble-sender">EcoTwin Copilot</div>
            <div class="bubble-content text-muted">
                <span class="pulse-dot" style="display: inline-block;"></span> Analyzing digital twin telemetry...
            </div>
        `;
        chatBox.appendChild(bubble);
        chatBox.scrollTop = chatBox.scrollHeight;
        return bubble;
    },

    formatMarkdown(text) {
        if (!text) return '';
        let html = text
            .replace(/### (.*?)\n/g, '<h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 6px; color: var(--text-primary);">$1</h4>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code style="background: rgba(0,0,0,0.3); padding: 1px 4px; border-radius: 3px; font-family: var(--font-mono); font-size: 0.78rem;">$1</code>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n- /g, '<br>&bull; ');
        return html;
    }
};
