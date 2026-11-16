/**
 * EcoTwin Main Controller & State Manager
 */

window.EcoTwin = {
    activeTab: 'twin-view',
    simSpeed: 1.0,
    state: null,
    
    init() {
        this.initTabs();
        this.initSimControls();
        this.initKeyModal();
        this.startSimHeartbeat();
        
        // Initialize sub-views
        if (window.TwinView) window.TwinView.init();
        if (window.CVView) window.CVView.init();
        if (window.CopilotView) window.CopilotView.init();
    },

    initTabs() {
        const tabs = document.querySelectorAll('.nav-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.tab;
                this.switchTab(target);
            });
        });
    },

    switchTab(tabId) {
        this.activeTab = tabId;
        document.querySelectorAll('.nav-tab').forEach(t => {
            t.classList.toggle('active', t.dataset.tab === tabId);
        });
        document.querySelectorAll('.tab-panel').forEach(p => {
            p.classList.toggle('active', p.id === tabId);
        });

        if (tabId === 'analytics-view') {
            this.loadAnalytics();
        } else if (tabId === 'twin-view' && window.TwinView) {
            window.TwinView.resizeCanvas();
        }
    },

    initSimControls() {
        // Speed buttons
        document.querySelectorAll('.sim-speed-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const speed = parseFloat(btn.dataset.speed);
                document.querySelectorAll('.sim-speed-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                try {
                    const res = await fetch('/api/twin/speed', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ speed })
                    });
                    const data = await res.json();
                    this.simSpeed = data.speed;
                } catch (e) {
                    console.error('Speed change error:', e);
                }
            });
        });

        // Scenario select
        const scenarioSelect = document.getElementById('scenario-select');
        if (scenarioSelect) {
            scenarioSelect.addEventListener('change', async (e) => {
                const scenario = e.target.value;
                try {
                    const res = await fetch('/api/twin/scenario', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ scenario })
                    });
                    const data = await res.json();
                    if (data.state) {
                        this.updateHeaderKPIs(data.state);
                        if (window.TwinView) window.TwinView.render(data.state);
                    }
                } catch (err) {
                    console.error('Scenario error:', err);
                }
            });
        }
    },

    initKeyModal() {
        const modal = document.getElementById('key-modal');
        const openBtn = document.getElementById('open-key-modal');
        const closeBtn = document.getElementById('close-key-modal');
        const saveBtn = document.getElementById('btn-save-key');
        const keyInput = document.getElementById('gemini-key-input');
        const statusMsg = document.getElementById('key-status-msg');

        if (openBtn) openBtn.onclick = () => modal.classList.remove('hidden');
        if (closeBtn) closeBtn.onclick = () => modal.classList.add('hidden');
        
        if (saveBtn) {
            saveBtn.onclick = async () => {
                const key = keyInput.value.trim();
                statusMsg.textContent = 'Configuring key...';
                statusMsg.className = 'text-sm text-blue';
                
                try {
                    const res = await fetch('/api/ai/set-key', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ api_key: key })
                    });
                    const data = await res.json();
                    if (data.success) {
                        statusMsg.textContent = 'Key verified! Multimodal vision & Gemini Copilot active.';
                        statusMsg.className = 'text-sm text-emerald';
                        setTimeout(() => modal.classList.add('hidden'), 1500);
                    } else {
                        statusMsg.textContent = data.error || 'Failed to set key';
                        statusMsg.className = 'text-sm text-red';
                    }
                } catch (e) {
                    statusMsg.textContent = 'Network error configuring key';
                    statusMsg.className = 'text-sm text-red';
                }
            };
        }
    },

    startSimHeartbeat() {
        // Step simulation every 1.5 seconds
        setInterval(async () => {
            try {
                const res = await fetch('/api/twin/step', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ delta_seconds: 15 })
                });
                const data = await res.json();
                if (data.success && data.state) {
                    this.state = data.state;
                    this.updateHeaderKPIs(data.state);
                    if (window.TwinView) window.TwinView.render(data.state);
                }
            } catch (err) {
                // Background quiet retry
            }
        }, 1500);
    },

    updateHeaderKPIs(state) {
        const kpis = state.kpis || {};
        const divEl = document.getElementById('hdr-diversion');
        const carbEl = document.getElementById('hdr-carbon');
        const critEl = document.getElementById('hdr-critical-bins');
        const fleetEl = document.getElementById('hdr-active-trucks');

        if (divEl) divEl.textContent = `${kpis.diversion_rate_pct || 0}%`;
        if (carbEl) carbEl.textContent = `${kpis.carbon_mitigated_tco2 || 0} t`;
        if (critEl) critEl.textContent = kpis.critical_bin_count || 0;
        if (fleetEl) fleetEl.textContent = `${kpis.active_truck_count || 0} / 4`;
    },

    async loadAnalytics() {
        try {
            const res = await fetch('/api/analytics');
            const data = await res.json();
            if (!data.success) return;
            const a = data.analytics;

            // Render Stream Bars
            const streamList = document.getElementById('stream-bars-list');
            if (streamList && a.stream_distribution) {
                streamList.innerHTML = Object.entries(a.stream_distribution).map(([cat, pct]) => `
                    <div class="stream-bar-item">
                        <div class="stream-bar-header">
                            <span>${cat}</span>
                            <strong>${pct}%</strong>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${pct}%;"></div>
                        </div>
                    </div>
                `).join('');
            }

            // Render Sector Table
            const secTable = document.getElementById('sector-table-body');
            if (secTable && a.sector_performance) {
                secTable.innerHTML = a.sector_performance.map(s => `
                    <tr>
                        <td><strong>${s.name}</strong></td>
                        <td>${s.avg_fill_pct}%</td>
                        <td><span class="${s.contamination_pct > 20 ? 'text-amber font-bold' : ''}">${s.contamination_pct}%</span></td>
                        <td>${s.critical_bins > 0 ? `<span class="badge badge-danger">${s.critical_bins} Bins</span>` : '0'}</td>
                        <td><span class="badge ${s.critical_bins > 0 ? 'badge-warning' : 'badge-success'}">${s.critical_bins > 0 ? 'Action Needed' : 'Nominal'}</span></td>
                    </tr>
                `).join('');
            }

            // Render Predictive Overflows
            const ofTable = document.getElementById('overflow-table-body');
            if (ofTable && a.top_overflow_risks) {
                ofTable.innerHTML = a.top_overflow_risks.map(o => `
                    <tr>
                        <td><strong>${o.bin_id}</strong></td>
                        <td>${o.sector}</td>
                        <td>${o.waste_type}</td>
                        <td>${o.current_fill}%</td>
                        <td><strong>${o.estimated_hours_to_overflow} hrs</strong></td>
                        <td><span class="badge ${o.risk_level_4h === 'CRITICAL' ? 'badge-danger' : (o.risk_level_4h === 'ELEVATED' ? 'badge-warning' : 'badge-info')}">${o.risk_level_4h}</span></td>
                        <td>
                            <button class="btn btn-xs btn-primary" onclick="EcoTwin.dispatchToBin('${o.bin_id}')">Dispatch</button>
                        </td>
                    </tr>
                `).join('');
            }
        } catch (e) {
            console.error('Failed to load analytics:', e);
        }
    },

    async dispatchToBin(binId) {
        try {
            const res = await fetch('/api/twin/dispatch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ truck_id: 'TRUCK-01', bin_ids: [binId] })
            });
            const data = await res.json();
            alert(data.message || `Dispatched to ${binId}`);
        } catch (e) {
            alert('Dispatch request failed');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.EcoTwin.init();
});
