/**
 * Computer Vision Waste Classifier & Optical Conveyor Controller
 */

window.CVView = {
    samples: [],
    activeSampleId: null,
    conveyorRunning: false,
    conveyorInterval: null,
    webcamStream: null,

    init() {
        this.loadSampleGallery();
        this.initModeToggles();
        this.initDropzone();
        this.initConveyor();
    },

    async loadSampleGallery() {
        try {
            const res = await fetch('/api/cv/gallery');
            const data = await res.json();
            if (data.success && data.samples) {
                this.samples = data.samples;
                this.renderSampleChips(data.samples);
                // Auto-select first sample for initial presentation
                if (data.samples.length > 0) {
                    this.selectSample(data.samples[0].id);
                }
            }
        } catch (e) {
            console.error('Failed to load CV samples:', e);
        }
    },

    renderSampleChips(samples) {
        const scroll = document.getElementById('samples-scroll');
        if (!scroll) return;

        scroll.innerHTML = samples.map(s => `
            <div class="sample-chip ${s.id === this.activeSampleId ? 'active' : ''}" 
                 id="chip-${s.id}" 
                 onclick="CVView.selectSample('${s.id}')">
                <div class="sample-chip-svg">${s.svg_icon}</div>
                <div class="sample-chip-name">${s.name}</div>
                <span class="badge ${s.is_contaminated ? 'badge-danger' : 'badge-success'}" style="font-size: 0.6rem; margin-top: 4px;">
                    ${s.is_contaminated ? 'Contaminated' : 'Clean'}
                </span>
            </div>
        `).join('');
    },

    async selectSample(sampleId) {
        this.activeSampleId = sampleId;
        document.querySelectorAll('.sample-chip').forEach(c => c.classList.remove('active'));
        const chip = document.getElementById(`chip-${sampleId}`);
        if (chip) chip.classList.add('active');

        const sample = this.samples.find(s => s.id === sampleId);
        if (!sample) return;

        // Render preview
        const preview = document.getElementById('cv-preview-container');
        if (preview) {
            preview.innerHTML = sample.svg_icon;
        }

        // Render bounding box
        this.renderBoundingBox(sample.bounding_box, sample.category, sample.confidence, sample.is_contaminated);

        // Run classification API
        try {
            const res = await fetch('/api/cv/classify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image: `sample:${sampleId}`,
                    features: {
                        avg_r: parseInt(sample.dominant_colors[0].slice(1, 3), 16),
                        avg_g: parseInt(sample.dominant_colors[0].slice(3, 5), 16),
                        avg_b: parseInt(sample.dominant_colors[0].slice(5, 7), 16),
                        brightness: 120,
                        aspect_ratio: 1.2
                    }
                })
            });
            const data = await res.json();
            if (data.success && data.result) {
                this.updateResultsCard(data.result);
            }
        } catch (e) {
            console.error('Classification error:', e);
        }
    },

    renderBoundingBox(bbox, label, confidence, isContaminated) {
        const overlay = document.getElementById('cv-bbox-overlay');
        if (!overlay || !bbox) return;

        // bbox is [ymin, xmin, ymax, xmax]
        const [ymin, xmin, ymax, xmax] = bbox;
        const top = (ymin * 100).toFixed(1);
        const left = (xmin * 100).toFixed(1);
        const width = ((xmax - xmin) * 100).toFixed(1);
        const height = ((ymax - ymin) * 100).toFixed(1);

        overlay.innerHTML = `
            <div class="bbox-rect" style="top: ${top}%; left: ${left}%; width: ${width}%; height: ${height}%; border-color: ${isContaminated ? '#EF4444' : '#10B981'};">
                <span class="bbox-label" style="background: ${isContaminated ? '#EF4444' : '#10B981'}; color: #FFFFFF;">
                    ${label} &bull; ${Math.round((confidence || 0.95) * 100)}%
                </span>
            </div>
        `;
    },

    updateResultsCard(result) {
        const catEl = document.getElementById('res-category');
        const nameEl = document.getElementById('res-item-name');
        const subEl = document.getElementById('res-subtype');
        const confEl = document.getElementById('res-confidence');
        const contamBadge = document.getElementById('res-contamination-badge');
        const scorePct = document.getElementById('res-score-pct');
        const scoreBar = document.getElementById('res-score-bar');
        const prepEl = document.getElementById('res-prep-text');
        const targetBin = document.getElementById('res-target-bin');
        const contamNotes = document.getElementById('res-contam-notes');
        const carbonEl = document.getElementById('res-carbon');
        const valEl = document.getElementById('res-val');
        const engineBadge = document.getElementById('cv-engine-badge');

        if (catEl) catEl.textContent = result.category;
        if (nameEl) nameEl.textContent = result.item_name;
        if (subEl) subEl.textContent = result.subtype || result.category;
        if (confEl) confEl.textContent = `Confidence: ${Math.round(result.confidence * 100)}%`;
        if (engineBadge) engineBadge.textContent = result.engine_used || 'CV Model';

        if (contamBadge) {
            contamBadge.textContent = result.is_contaminated ? '⚠️ Contaminated' : '✓ Clean Stream';
            contamBadge.className = `badge ${result.is_contaminated ? 'badge-danger' : 'badge-success'}`;
        }

        const score = result.recyclability_score || (result.is_contaminated ? 15 : 90);
        if (scorePct) scorePct.textContent = `${score}%`;
        if (scoreBar) {
            scoreBar.style.width = `${score}%`;
            scoreBar.style.background = score > 70 ? 'linear-gradient(90deg, #3B82F6, #10B981)' : (score > 30 ? '#F59E0B' : '#EF4444');
        }

        if (prepEl) prepEl.textContent = result.prep_instructions || 'Clean and bin appropriately.';
        if (targetBin) targetBin.textContent = result.target_bin || 'Recyclables Bin';
        if (contamNotes) contamNotes.textContent = result.contamination_notes || 'No foreign contaminants detected.';

        if (carbonEl) carbonEl.textContent = `${result.carbon_saved_kg || 0.05} kg CO₂e`;
        if (valEl) valEl.textContent = `$${(result.commodity_value_usd || 0.01).toFixed(4)}`;
    },

    initModeToggles() {
        const btnSamples = document.getElementById('btn-mode-samples');
        const btnUpload = document.getElementById('btn-mode-upload');
        const btnWebcam = document.getElementById('btn-mode-webcam');

        const uploadBox = document.getElementById('upload-box');
        const webcamBox = document.getElementById('webcam-box');
        const previewWrap = document.querySelector('.cv-canvas-wrap');

        const resetModes = () => {
            [btnSamples, btnUpload, btnWebcam].forEach(b => b && b.classList.remove('active'));
            if (uploadBox) uploadBox.classList.add('hidden');
            if (webcamBox) webcamBox.classList.add('hidden');
            this.stopWebcam();
        };

        if (btnSamples) {
            btnSamples.onclick = () => {
                resetModes();
                btnSamples.classList.add('active');
                if (this.activeSampleId) this.selectSample(this.activeSampleId);
            };
        }

        if (btnUpload) {
            btnUpload.onclick = () => {
                resetModes();
                btnUpload.classList.add('active');
                if (uploadBox) uploadBox.classList.remove('hidden');
            };
        }

        if (btnWebcam) {
            btnWebcam.onclick = () => {
                resetModes();
                btnWebcam.classList.add('active');
                if (webcamBox) webcamBox.classList.remove('hidden');
                this.startWebcam();
            };
        }

        // Webcam buttons
        const captureBtn = document.getElementById('btn-capture-webcam');
        const stopBtn = document.getElementById('btn-stop-webcam');
        if (captureBtn) captureBtn.onclick = () => this.captureWebcamFrame();
        if (stopBtn) stopBtn.onclick = () => {
            resetModes();
            btnSamples.classList.add('active');
            if (this.activeSampleId) this.selectSample(this.activeSampleId);
        };
    },

    initDropzone() {
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('file-input');
        if (!dropzone || !fileInput) return;

        dropzone.onclick = () => fileInput.click();

        dropzone.ondragover = (e) => {
            e.preventDefault();
            dropzone.style.borderColor = '#10B981';
        };

        dropzone.ondragleave = () => {
            dropzone.style.borderColor = '#3B82F6';
        };

        dropzone.ondrop = (e) => {
            e.preventDefault();
            dropzone.style.borderColor = '#3B82F6';
            if (e.dataTransfer.files.length) {
                this.handleImageFile(e.dataTransfer.files[0]);
            }
        };

        fileInput.onchange = (e) => {
            if (e.target.files.length) {
                this.handleImageFile(e.target.files[0]);
            }
        };
    },

    handleImageFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const dataUrl = e.target.result;
            this.processUploadedImage(dataUrl, file.name);
        };
        reader.readAsDataURL(file);
    },

    processUploadedImage(dataUrl, filename) {
        // Render image in preview
        const preview = document.getElementById('cv-preview-container');
        if (preview) {
            preview.innerHTML = `<img src="${dataUrl}" style="max-width: 260px; max-height: 260px; object-fit: contain; border-radius: 8px;">`;
        }

        // Hide upload box, show preview
        const uploadBox = document.getElementById('upload-box');
        if (uploadBox) uploadBox.classList.add('hidden');

        // Extract basic color features with canvas
        const img = new Image();
        img.onload = async () => {
            const canvas = document.createElement('canvas');
            canvas.width = 32;
            canvas.height = 32;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, 32, 32);
            const imgData = ctx.getImageData(0, 0, 32, 32).data;

            let r = 0, g = 0, b = 0;
            for (let i = 0; i < imgData.length; i += 4) {
                r += imgData[i];
                g += imgData[i + 1];
                b += imgData[i + 2];
            }
            const count = imgData.length / 4;
            const avgR = Math.round(r / count);
            const avgG = Math.round(g / count);
            const avgB = Math.round(b / count);
            const brightness = Math.round((avgR * 299 + avgG * 587 + avgB * 114) / 1000);

            try {
                const res = await fetch('/api/cv/classify', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: dataUrl,
                        features: {
                            avg_r: avgR,
                            avg_g: avgG,
                            avg_b: avgB,
                            brightness: brightness,
                            aspect_ratio: img.width / img.height
                        }
                    })
                });
                const data = await res.json();
                if (data.success && data.result) {
                    this.updateResultsCard(data.result);
                    this.renderBoundingBox(data.result.bounding_box, data.result.category, data.result.confidence, data.result.is_contaminated);
                }
            } catch (err) {
                console.error('Inference error:', err);
            }
        };
        img.src = dataUrl;
    },

    async startWebcam() {
        const video = document.getElementById('webcam-video');
        if (!video) return;

        try {
            this.webcamStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
            video.srcObject = this.webcamStream;
        } catch (e) {
            alert('Could not access webcam. Please allow camera permissions or upload an image.');
        }
    },

    stopWebcam() {
        if (this.webcamStream) {
            this.webcamStream.getTracks().forEach(t => t.stop());
            this.webcamStream = null;
        }
    },

    captureWebcamFrame() {
        const video = document.getElementById('webcam-video');
        if (!video) return;

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const dataUrl = canvas.toDataURL('image/jpeg');
        this.stopWebcam();
        const webcamBox = document.getElementById('webcam-box');
        if (webcamBox) webcamBox.classList.add('hidden');

        this.processUploadedImage(dataUrl, 'webcam_capture.jpg');
    },

    initConveyor() {
        const btn = document.getElementById('btn-toggle-conveyor');
        if (!btn) return;

        btn.onclick = () => {
            this.conveyorRunning = !this.conveyorRunning;
            if (this.conveyorRunning) {
                btn.textContent = '⏹ Stop Optical Stream';
                btn.classList.add('active');
                this.stepConveyor();
                this.conveyorInterval = setInterval(() => this.stepConveyor(), 2200);
            } else {
                btn.textContent = '▶ Start Optical Stream';
                btn.classList.remove('active');
                clearInterval(this.conveyorInterval);
            }
        };
    },

    async stepConveyor() {
        try {
            const res = await fetch('/api/cv/conveyor/step');
            const data = await res.json();
            if (data.success && data.item) {
                const item = data.item;
                const activeItem = document.getElementById('conveyor-active-item');
                const countEl = document.getElementById('conveyor-count');
                const ejectedEl = document.getElementById('conveyor-ejected');

                if (countEl) countEl.textContent = data.total_items_scanned;
                if (ejectedEl) ejectedEl.textContent = data.contaminants_ejected;

                if (activeItem) {
                    activeItem.innerHTML = `
                        <span style="color: ${item.is_contaminated ? '#EF4444' : '#10B981'}; font-weight: 700;">
                            ${item.item_name} &bull; ${item.pneumatic_actuator === 'FIRE_JET' ? '⚡ Routed to ' + item.target_bunker : '🚨 PNEUMATIC EJECT'}
                        </span>
                    `;
                }
            }
        } catch (e) {
            console.error('Conveyor step error:', e);
        }
    }
};
