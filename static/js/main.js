// Truck Maintenance System - Global JavaScript Utilities

document.addEventListener('DOMContentLoaded', function() {
    // 1. Auto-dismiss Bootstrap alert toasts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                if (bsAlert) bsAlert.close();
            } catch (e) {}
        }, 6000);
    });

    // 2. Global Quick Search in Header
    const searchInput = document.getElementById('globalSearchInput');
    const searchDropdown = document.getElementById('globalSearchResults');

    if (searchInput && searchDropdown) {
        let debounceTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const query = this.value.trim();
            if (query.length < 2) {
                searchDropdown.style.display = 'none';
                searchDropdown.innerHTML = '';
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/api/search?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.results && data.results.length > 0) {
                            let html = '';
                            data.results.forEach(item => {
                                let badgeColor = 'bg-primary';
                                if (item.category === 'Driver') badgeColor = 'bg-info text-dark';
                                if (item.category === 'Vehicle') badgeColor = 'bg-warning text-dark';
                                if (item.category === 'Memo') badgeColor = 'bg-success';
                                if (item.category === 'Customer') badgeColor = 'bg-purple';

                                html += `
                                    <a href="${item.url}" class="search-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <div class="fw-bold fs-7">${item.title}</div>
                                            <div class="text-muted small">${item.subtitle}</div>
                                        </div>
                                        <span class="badge ${badgeColor} rounded-pill">${item.category}</span>
                                    </a>
                                `;
                            });
                            searchDropdown.innerHTML = html;
                            searchDropdown.style.display = 'block';
                        } else {
                            searchDropdown.innerHTML = '<div class="p-3 text-center text-muted small">No matching records found</div>';
                            searchDropdown.style.display = 'block';
                        }
                    })
                    .catch(err => {
                        console.error("Search error:", err);
                    });
            }, 250);
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
                searchDropdown.style.display = 'none';
            }
        });
    }
});
