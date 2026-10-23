// Interactive Financial Calculator & Memo OCR Verification Helper

function parseNumber(val) {
    if (!val) return 0.0;
    const clean = String(val).replace(/[^0-9.-]/g, '');
    const num = parseFloat(clean);
    return isNaN(num) ? 0.0 : num;
}

function formatINR(val) {
    return '₹' + Number(val).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function recalculateFinancials() {
    const freight = parseNumber(document.getElementById('freight_amount')?.value);
    const advance = parseNumber(document.getElementById('advance_amount')?.value);
    const diesel = parseNumber(document.getElementById('diesel_expense')?.value);
    const toll = parseNumber(document.getElementById('toll_expense')?.value);
    const food = parseNumber(document.getElementById('food_expense')?.value);
    const loading = parseNumber(document.getElementById('loading_charges')?.value);
    const unloading = parseNumber(document.getElementById('unloading_charges')?.value);
    const commission = parseNumber(document.getElementById('commission_expense')?.value);
    const other = parseNumber(document.getElementById('other_expenses')?.value);

    // Total Operating Expense
    const totalExpense = diesel + toll + food + loading + unloading + commission + other;
    // Profit = Freight - Total Expense
    const profit = freight - totalExpense;
    // Net Amount = Freight - Advance - Total Expense
    const netAmount = freight - advance - totalExpense;

    // Update Display Elements
    const totalExpDisplay = document.getElementById('display_total_expense');
    const profitDisplay = document.getElementById('display_profit');
    const netDisplay = document.getElementById('display_net_amount');
    const statusBadge = document.getElementById('display_status_badge');

    if (totalExpDisplay) totalExpDisplay.innerText = formatINR(totalExpense);
    if (netDisplay) netDisplay.innerText = formatINR(netAmount);

    if (profitDisplay) {
        profitDisplay.innerText = formatINR(profit);
        if (profit >= 0) {
            profitDisplay.className = 'fw-bold text-success fs-5';
        } else {
            profitDisplay.className = 'fw-bold text-danger fs-5';
        }
    }

    if (statusBadge) {
        if (profit >= 0) {
            statusBadge.innerText = 'STATUS: PROFIT';
            statusBadge.className = 'badge bg-success px-3 py-1 rounded-pill';
        } else {
            statusBadge.innerText = 'STATUS: LOSS';
            statusBadge.className = 'badge bg-danger px-3 py-1 rounded-pill';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 1. Attach live recalculation triggers
    const inputIds = [
        'freight_amount', 'advance_amount', 'diesel_expense',
        'toll_expense', 'food_expense', 'loading_charges',
        'unloading_charges', 'commission_expense', 'other_expenses'
    ];

    inputIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', recalculateFinancials);
            el.addEventListener('change', recalculateFinancials);
        }
    });

    // Initial calculation on load
    recalculateFinancials();

    // 2. Image Zoom & Pan functionality
    let currentZoom = 1.0;
    let currentRotation = 0;
    const zoomImg = document.getElementById('previewMemoImg');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const zoomResetBtn = document.getElementById('zoomResetBtn');
    const rotateBtn = document.getElementById('rotateBtn');
    const imageContainer = document.getElementById('imageContainer');
    const highlightBox = document.getElementById('highlightBox');

    function applyTransform() {
        if (zoomImg) {
            zoomImg.style.transform = `scale(${currentZoom}) rotate(${currentRotation}deg)`;
        }
    }

    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', () => {
            currentZoom = Math.min(currentZoom + 0.25, 3.5);
            applyTransform();
        });
    }

    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', () => {
            currentZoom = Math.max(currentZoom - 0.25, 0.5);
            applyTransform();
        });
    }

    if (zoomResetBtn) {
        zoomResetBtn.addEventListener('click', () => {
            currentZoom = 1.0;
            currentRotation = 0;
            applyTransform();
        });
    }

    const rotateLeftBtn = document.getElementById('rotateLeftBtn');
    if (rotateLeftBtn) {
        rotateLeftBtn.addEventListener('click', () => {
            currentRotation = (currentRotation - 90 + 360) % 360;
            applyTransform();
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener('click', () => {
            currentRotation = (currentRotation + 90) % 360;
            applyTransform();
        });
    }

    // 2b. Server Re-Scan Orientation
    const btnRescan = document.getElementById('btnRescanOrientation');
    if (btnRescan) {
        btnRescan.addEventListener('click', async () => {
            if (currentRotation === 0) {
                alert('Please click Rotate Left or Rotate Right to adjust the image orientation first, then click Re-Scan.');
                return;
            }
            const origSrc = zoomImg.getAttribute('data-original') || zoomImg.src;
            btnRescan.disabled = true;
            btnRescan.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin me-1"></i> Re-Scanning...';

            try {
                const response = await fetch('/driver/memos/rescan_orientation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image_rel_path: origSrc,
                        angle: currentRotation
                    })
                });
                const result = await response.json();
                if (result.success && result.data) {
                    currentRotation = 0;
                    applyTransform();

                    if (result.enhanced_image_url) {
                        zoomImg.src = result.enhanced_image_url;
                        zoomImg.setAttribute('data-enhanced', result.enhanced_image_url);
                    }
                    if (result.original_image_url) {
                        zoomImg.setAttribute('data-original', result.original_image_url);
                    }
                    if (result.binarized_image_url) {
                        zoomImg.setAttribute('data-binarized', result.binarized_image_url);
                    }

                    const d = result.data;
                    const setVal = (id, val) => {
                        const el = document.getElementById(id);
                        if (el && val !== undefined && val !== null) el.value = val;
                    };
                    setVal('field_memo_number', d.memo_number);
                    setVal('field_memo_date', d.date);
                    setVal('field_vehicle_number', d.vehicle_number);
                    setVal('field_driver_name', d.driver_name);
                    setVal('field_driver_phone', d.driver_phone);
                    setVal('field_source', d.starting_location || d.source);
                    setVal('field_destination', d.destination);
                    setVal('freight_amount', d.freight_amount || d.trip_amount);
                    setVal('advance_amount', d.driver_advance);
                    setVal('diesel_expense', d.fuel_expense);
                    setVal('toll_expense', d.toll_expense);
                    setVal('food_expense', d.food_expense);
                    setVal('loading_charges', d.loading_charge);
                    setVal('unloading_charges', d.unloading_charge);
                    setVal('other_expenses', d.other_expense);

                    if (window.renderTableRows && d.table_rows) {
                        window.renderTableRows(d.table_rows);
                    }

                    if (typeof recalculateFinancials === 'function') {
                        recalculateFinancials();
                    }

                    alert('✓ Memo re-scanned successfully with new orientation! Extracted details and spreadsheet updated.');
                } else {
                    alert('Re-scan error: ' + (result.error || 'Failed to extract details.'));
                }
            } catch (err) {
                alert('Network or server error during re-scan: ' + err.message);
            } finally {
                btnRescan.disabled = false;
                btnRescan.innerHTML = '<i class="fa-solid fa-arrows-rotate me-1"></i> Re-Scan Orientation';
            }
        });
    }

    // 3. Interactive Field-to-Image Bounding Box Highlighting
    let fieldBoxes = {};
    const boxesScript = document.getElementById('fieldBoxesData');
    if (boxesScript) {
        try {
            fieldBoxes = JSON.parse(boxesScript.textContent.trim());
        } catch (e) {
            console.warn("Could not parse fieldBoxesData:", e);
        }
    }

    function showFieldHighlight(fieldName) {
        if (!highlightBox || !zoomImg) return;
        const box = fieldBoxes[fieldName];
        if (box && box.length === 4) {
            const [ymin, xmin, ymax, xmax] = box;
            if (ymax > ymin && xmax > xmin) {
                // Position overlay relative to the image container
                const rect = zoomImg.getBoundingClientRect();
                const containerRect = imageContainer.getBoundingClientRect();

                const imgLeft = zoomImg.offsetLeft;
                const imgTop = zoomImg.offsetTop;
                const imgWidth = zoomImg.offsetWidth;
                const imgHeight = zoomImg.offsetHeight;

                highlightBox.style.left = `${imgLeft + (xmin * imgWidth)}px`;
                highlightBox.style.top = `${imgTop + (ymin * imgHeight)}px`;
                highlightBox.style.width = `${Math.max((xmax - xmin) * imgWidth, 30)}px`;
                highlightBox.style.height = `${Math.max((ymax - ymin) * imgHeight, 20)}px`;
                highlightBox.classList.remove('d-none');
                return;
            }
        }
        highlightBox.classList.add('d-none');
    }

    function hideFieldHighlight() {
        if (highlightBox) {
            highlightBox.classList.add('d-none');
        }
    }

    // Attach focus and hover listeners to all form fields with data-field attribute
    const interactiveInputs = document.querySelectorAll('[data-field]');
    interactiveInputs.forEach(input => {
        const fieldName = input.getAttribute('data-field');
        input.addEventListener('focus', () => showFieldHighlight(fieldName));
        input.addEventListener('mouseenter', () => showFieldHighlight(fieldName));
        input.addEventListener('blur', hideFieldHighlight);
        input.addEventListener('mouseleave', () => {
            if (document.activeElement !== input) {
                hideFieldHighlight();
            }
        });
    });
});
