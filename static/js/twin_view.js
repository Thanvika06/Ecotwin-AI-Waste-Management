/**
 * Interactive Digital Twin Geospatial Canvas & Fleet Controller
 */

window.TwinView = {
    canvas: null,
    ctx: null,
    state: null,
    selectedEntity: null,
    hoveredEntity: null,
    animationFrameId: null,

    init() {
        this.canvas = document.getElementById('digitalTwinCanvas');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());

        this.initInteractions();
        this.initAutoDispatch();
    },

    resizeCanvas() {
        if (!this.canvas) return;
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width || 800;
        this.canvas.height = rect.height || 640;
        if (this.state) this.render(this.state);
    },

    initInteractions() {
        const tooltip = document.getElementById('twin-tooltip');

        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const scaleX = 800 / this.canvas.width;
            const scaleY = 640 / this.canvas.height;
            const mx = (e.clientX - rect.left) * scaleX;
            const my = (e.clientY - rect.top) * scaleY;

            this.hoveredEntity = this.findEntityAt(mx, my);

            if (this.hoveredEntity && tooltip) {
                tooltip.classList.remove('hidden');
                tooltip.style.left = `${e.clientX - rect.left + 15}px`;
                tooltip.style.top = `${e.clientY - rect.top - 15}px`;

                if (this.hoveredEntity.type === 'bin') {
                    const b = this.hoveredEntity.data;
                    tooltip.innerHTML = `
                        <strong>${b.id}</strong> (${b.waste_type})<br>
                        Fill: <span class="${b.current_fill_pct >= 85 ? 'text-red' : 'text-emerald'}">${b.current_fill_pct}%</span><br>
                        Sector: ${b.sector_name}<br>
                        Temp: ${b.temperature_c}°C | Battery: ${b.battery_pct}%
                    `;
                } else if (this.hoveredEntity.type === 'truck') {
                    const t = this.hoveredEntity.data;
                    tooltip.innerHTML = `
                        <strong>${t.name}</strong> (${t.id})<br>
                        Status: ${t.status}<br>
                        Load: ${t.load_pct}% (${t.current_load_tons}t)<br>
                        Power: ${t.fuel_or_battery_pct}%
                    `;
                } else if (this.hoveredEntity.type === 'facility') {
                    const f = this.hoveredEntity.data;
                    tooltip.innerHTML = `
                        <strong>${f.name}</strong><br>
                        Type: ${f.type}<br>
                        Storage: ${f.current_stored_tons} / ${f.capacity_tons_day} tons
                    `;
                }
            } else if (tooltip) {
                tooltip.classList.add('hidden');
            }
        });

        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const scaleX = 800 / this.canvas.width;
            const scaleY = 640 / this.canvas.height;
            const mx = (e.clientX - rect.left) * scaleX;
            const my = (e.clientY - rect.top) * scaleY;

            const clicked = this.findEntityAt(mx, my);
            if (clicked) {
                this.selectedEntity = clicked;
                this.updateInspector(clicked);
            }
        });
    },

    findEntityAt(x, y) {
        if (!this.state) return null;

        // Check trucks (radius ~ 18)
        for (const t of (this.state.trucks || [])) {
            const dx = t.coords.x - x;
            const dy = t.coords.y - y;
            if (Math.hypot(dx, dy) < 22) return { type: 'truck', data: t };
        }

        // Check bins (radius ~ 12)
        for (const b of (this.state.bins || [])) {
            const dx = b.coords.x - x;
            const dy = b.coords.y - y;
            if (Math.hypot(dx, dy) < 16) return { type: 'bin', data: b };
        }

        // Check facilities (radius ~ 26)
        for (const f of (this.state.facilities || [])) {
            const dx = f.coords.x - x;
            const dy = f.coords.y - y;
            if (Math.hypot(dx, dy) < 28) return { type: 'facility', data: f };
        }

        return null;
    },

    initAutoDispatch() {
        const btn = document.getElementById('btn-auto-dispatch');
        if (btn) {
            btn.onclick = async () => {
                try {
                    const res = await fetch('/api/twin/dispatch', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ truck_id: 'TRUCK-01' })
                    });
                    const data = await res.json();
                    alert(data.message || 'Auto-dispatch initiated!');
                } catch (e) {
                    alert('Dispatch failed');
                }
            };
        }
    },

    render(state) {
        this.state = state;
        if (!this.ctx) return;

        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;
        const scaleX = w / 800;
        const scaleY = h / 640;

        ctx.save();
        ctx.scale(scaleX, scaleY);

        // 1. Clear background
        ctx.fillStyle = '#080C14';
        ctx.fillRect(0, 0, 800, 640);

        // 2. Draw Road Grid Network
        this.drawRoadNetwork(ctx);

        // 3. Draw Sectors
        this.drawSectors(ctx, state.sectors || []);

        // 4. Draw Facilities
        this.drawFacilities(ctx, state.facilities || []);

        // 5. Draw Smart Bins
        this.drawBins(ctx, state.bins || []);

        // 6. Draw Trucks and Dynamic Route Lines
        this.drawTrucks(ctx, state.trucks || []);

        ctx.restore();

        // Render side panels
        this.renderFleetStrip(state.trucks || []);
        this.renderFacilityList(state.facilities || []);
        this.renderAlertList(state.alerts || []);
    },

    drawRoadNetwork(ctx) {
        ctx.strokeStyle = '#1E293B';
        ctx.lineWidth = 14;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        const highways = [
            // Outer ring
            [[100, 100], [720, 100], [720, 560], [100, 560], [100, 100]],
            // Cross thoroughfares
            [[100, 320], [720, 320]],
            [[410, 100], [410, 560]],
            // Arterials
            [[250, 200], [410, 320], [550, 180]],
            [[220, 420], [410, 320], [620, 420]],
            [[410, 320], [400, 550]]
        ];

        highways.forEach(path => {
            ctx.beginPath();
            ctx.moveTo(path[0][0], path[0][1]);
            for (let i = 1; i < path.length; i++) {
                ctx.lineTo(path[i][0], path[i][1]);
            }
            ctx.stroke();
        });

        // Lane markings (dashed center)
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([8, 8]);
        highways.forEach(path => {
            ctx.beginPath();
            ctx.moveTo(path[0][0], path[0][1]);
            for (let i = 1; i < path.length; i++) {
                ctx.lineTo(path[i][0], path[i][1]);
            }
            ctx.stroke();
        });
        ctx.setLineDash([]);
    },

    drawSectors(ctx, sectors) {
        sectors.forEach(sec => {
            const cx = sec.center.x;
            const cy = sec.center.y;

            // Ambient sector glow
            const radGrad = ctx.createRadialGradient(cx, cy, 20, cx, cy, 90);
            radGrad.addColorStop(0, `${sec.color}18`);
            radGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = radGrad;
            ctx.beginPath();
            ctx.arc(cx, cy, 90, 0, Math.PI * 2);
            ctx.fill();

            // Label
            ctx.fillStyle = '#64748B';
            ctx.font = '600 11px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(sec.name.toUpperCase(), cx, cy - 65);
        });
    },

    drawFacilities(ctx, facilities) {
        facilities.forEach(fac => {
            const x = fac.coords.x;
            const y = fac.coords.y;

            // Outer ring
            ctx.fillStyle = '#0F172A';
            ctx.strokeStyle = fac.color || '#3B82F6';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.arc(x, y, 22, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();

            // Inner icon symbol
            ctx.fillStyle = fac.color || '#3B82F6';
            ctx.font = '700 11px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(fac.type.slice(0, 3), x, y);

            // Label tag below
            ctx.fillStyle = '#CBD5E1';
            ctx.font = '600 10px Inter, sans-serif';
            ctx.fillText(fac.name.split(' ')[0], x, y + 32);
        });
    },

    drawBins(ctx, bins) {
        bins.forEach(bin => {
            const x = bin.coords.x;
            const y = bin.coords.y;
            const fill = bin.current_fill_pct;
            const isCrit = fill >= 85;
            const isWarn = fill >= 70 && !isCrit;

            // Warning / Critical pulse aura
            if (isCrit) {
                ctx.fillStyle = 'rgba(239, 68, 68, 0.25)';
                ctx.beginPath();
                ctx.arc(x, y, 16, 0, Math.PI * 2);
                ctx.fill();
            }

            // Base bin circle
            ctx.fillStyle = '#1E293B';
            ctx.beginPath();
            ctx.arc(x, y, 9, 0, Math.PI * 2);
            ctx.fill();

            // Fill arc ring
            const endAngle = (fill / 100) * (Math.PI * 2) - Math.PI / 2;
            ctx.strokeStyle = isCrit ? '#EF4444' : (isWarn ? '#F59E0B' : '#10B981');
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(x, y, 9, -Math.PI / 2, endAngle);
            ctx.stroke();

            // Inner dot indicating waste category
            ctx.fillStyle = bin.color || '#38BDF8';
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
        });
    },

    drawTrucks(ctx, trucks) {
        trucks.forEach(truck => {
            const x = truck.coords.x;
            const y = truck.coords.y;

            // Draw route queue line to target bin
            if (truck.target_bin_id && this.state.bins) {
                const target = this.state.bins.find(b => b.id === truck.target_bin_id);
                if (target) {
                    ctx.strokeStyle = truck.color || '#38BDF8';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    ctx.lineTo(target.coords.x, target.coords.y);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }
            }

            // Draw Truck body
            ctx.fillStyle = truck.color || '#3B82F6';
            ctx.shadowColor = truck.color;
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.roundRect(x - 12, y - 8, 24, 16, 4);
            ctx.fill();
            ctx.shadowBlur = 0;

            // Truck cab
            ctx.fillStyle = '#0F172A';
            ctx.fillRect(x + 4, y - 6, 6, 12);

            // Load indicator bar above truck
            ctx.fillStyle = '#334155';
            ctx.fillRect(x - 12, y - 14, 24, 3);
            ctx.fillStyle = truck.load_pct > 80 ? '#EF4444' : '#10B981';
            ctx.fillRect(x - 12, y - 14, (truck.load_pct / 100) * 24, 3);

            // Truck label
            ctx.fillStyle = '#FFFFFF';
            ctx.font = '700 8px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(truck.id.slice(-2), x - 2, y + 3);
        });
    },

    renderFleetStrip(trucks) {
        const strip = document.getElementById('fleet-strip');
        if (!strip) return;

        strip.innerHTML = trucks.map(t => `
            <div class="truck-card-mini" onclick="TwinView.inspectTruck('${t.id}')">
                <div class="truck-title-row">
                    <span style="color: ${t.color}">${t.name.split(' ')[0]}</span>
                    <span class="badge ${t.status === 'EN_ROUTE' ? 'badge-warning' : (t.status === 'IDLE' ? '' : 'badge-info')}">${t.status}</span>
                </div>
                <div class="truck-meta">
                    Load: <strong>${t.load_pct}%</strong> (${t.current_load_tons}t) | Bat: <strong>${t.fuel_or_battery_pct}%</strong>
                </div>
                <div class="progress-bar" style="height: 4px;">
                    <div class="progress-fill" style="width: ${t.load_pct}%; background: ${t.color};"></div>
                </div>
            </div>
        `).join('');
    },

    renderFacilityList(facilities) {
        const list = document.getElementById('facility-list');
        if (!list) return;

        list.innerHTML = facilities.map(f => `
            <div class="facility-item">
                <div class="fac-title">
                    <span style="color: ${f.color}">${f.name}</span>
                    <span class="badge badge-info">${f.type}</span>
                </div>
                <div class="fac-stat">
                    Capacity: <strong>${f.current_stored_tons} / ${f.capacity_tons_day} tons</strong> (${Math.round((f.current_stored_tons/f.capacity_tons_day)*100)}%)
                </div>
                <div class="progress-bar" style="height: 4px;">
                    <div class="progress-fill" style="width: ${Math.round((f.current_stored_tons/f.capacity_tons_day)*100)}%; background: ${f.color};"></div>
                </div>
            </div>
        `).join('');
    },

    renderAlertList(alerts) {
        const list = document.getElementById('alert-list');
        const badge = document.getElementById('alert-count-badge');
        if (badge) badge.textContent = alerts.length;
        if (!list) return;

        if (alerts.length === 0) {
            list.innerHTML = `<div class="text-xs text-muted" style="padding: 8px;">No active alerts. Ecosystem nominal.</div>`;
            return;
        }

        list.innerHTML = alerts.map(a => `
            <div class="alert-item ${a.level}">
                <strong>${a.title}</strong>
                <div>${a.message}</div>
                <span class="text-xs text-muted">${a.timestamp}</span>
            </div>
        `).join('');
    },

    inspectTruck(truckId) {
        if (!this.state) return;
        const truck = this.state.trucks.find(t => t.id === truckId);
        if (truck) {
            this.selectedEntity = { type: 'truck', data: truck };
            this.updateInspector(this.selectedEntity);
        }
    },

    updateInspector(entity) {
        const body = document.getElementById('inspector-body');
        const badge = document.getElementById('inspector-badge');
        if (!body) return;

        if (entity.type === 'bin') {
            const b = entity.data;
            if (badge) {
                badge.textContent = b.id;
                badge.className = `badge ${b.current_fill_pct >= 85 ? 'badge-danger' : (b.current_fill_pct >= 70 ? 'badge-warning' : 'badge-success')}`;
            }
            body.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.8rem;">
                    <div><strong>Type:</strong> ${b.waste_type}</div>
                    <div><strong>Location:</strong> ${b.sector_name} (${b.coords.x}, ${b.coords.y})</div>
                    <div><strong>Fill Level:</strong> <strong class="${b.current_fill_pct >= 85 ? 'text-red' : 'text-emerald'}">${b.current_fill_pct}%</strong> (${Math.round(b.current_fill_pct * b.capacity_liters / 100)} / ${b.capacity_liters} L)</div>
                    <div><strong>Fill Rate:</strong> ${b.fill_rate_lph} Liters/hr</div>
                    <div><strong>Contamination:</strong> ${b.contamination_pct}%</div>
                    <div><strong>Temperature:</strong> ${b.temperature_c}°C</div>
                    <div><strong>Battery:</strong> ${b.battery_pct}%</div>
                    <div><strong>Last Serviced:</strong> ${b.last_serviced_min_ago} mins ago</div>
                    <div style="margin-top: 10px; display: flex; gap: 8px;">
                        <button class="btn btn-sm btn-primary" onclick="EcoTwin.dispatchToBin('${b.id}')">Dispatch Truck Here</button>
                    </div>
                </div>
            `;
        } else if (entity.type === 'truck') {
            const t = entity.data;
            if (badge) {
                badge.textContent = t.id;
                badge.className = 'badge badge-info';
            }
            body.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.8rem;">
                    <div><strong>Name:</strong> ${t.name}</div>
                    <div><strong>Type:</strong> ${t.type}</div>
                    <div><strong>Category:</strong> ${t.service_category}</div>
                    <div><strong>Status:</strong> <span class="badge badge-warning">${t.status}</span></div>
                    <div><strong>Load:</strong> ${t.load_pct}% (${t.current_load_tons} / ${t.capacity_tons} tons)</div>
                    <div><strong>Battery/Fuel:</strong> ${t.fuel_or_battery_pct}%</div>
                    <div><strong>CO₂ Mitigated:</strong> ${t.co2_saved_kg} kg</div>
                    <div><strong>Target Bin:</strong> ${t.target_bin_id || 'None'}</div>
                    <div style="margin-top: 10px;">
                        <button class="btn btn-sm btn-primary" onclick="TwinView.dispatchSpecificTruck('${t.id}')">Trigger Auto-Route</button>
                    </div>
                </div>
            `;
        }
    },

    async dispatchSpecificTruck(truckId) {
        try {
            const res = await fetch('/api/twin/dispatch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ truck_id: truckId })
            });
            const data = await res.json();
            alert(data.message || `Dispatched ${truckId}`);
        } catch (e) {
            alert('Dispatch failed');
        }
    }
};
