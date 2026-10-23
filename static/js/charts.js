// Truck Maintenance System - Dynamic Analytics Charts (Chart.js)

document.addEventListener('DOMContentLoaded', function() {
    const chartsContainer = document.getElementById('analyticsDashboardWrapper');
    if (!chartsContainer) return; // Only runs on pages with analytics

    fetch('/api/analytics/charts')
        .then(res => res.json())
        .then(data => {
            initMonthlyCharts(data);
            initVehicleCharts(data);
            initDriverAndFuelCharts(data);
            initProfitExpenseComparison(data);
        })
        .catch(err => console.error("Error fetching analytics data:", err));
});

// Common Chart.js styling options
const baseChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#94A3B8',
                font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 }
            }
        },
        tooltip: {
            backgroundColor: '#1E293B',
            titleColor: '#FFFFFF',
            bodyColor: '#94A3B8',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 10,
            boxPadding: 4,
            usePointStyle: true,
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) label += ': ';
                    if (context.parsed.y !== null) {
                        label += '₹' + Number(context.parsed.y).toLocaleString('en-IN');
                    }
                    return label;
                }
            }
        }
    },
    scales: {
        x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
            ticks: { color: '#64748B', font: { family: 'Plus Jakarta Sans', size: 11 } }
        },
        y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
            ticks: {
                color: '#64748B',
                font: { family: 'Plus Jakarta Sans', size: 11 },
                callback: function(value) {
                    if (value >= 1000) return '₹' + (value / 1000) + 'k';
                    return '₹' + value;
                }
            }
        }
    }
};

// 1, 2, 3: Monthly Revenue, Expense, Profit Charts
function initMonthlyCharts(data) {
    // 1. Monthly Revenue Chart
    const revCtx = document.getElementById('monthlyRevenueChart')?.getContext('2d');
    if (revCtx) {
        new Chart(revCtx, {
            type: 'line',
            data: {
                labels: data.months,
                datasets: [{
                    label: 'Revenue (INR)',
                    data: data.monthly_revenue,
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.15)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#3B82F6'
                }]
            },
            options: baseChartOptions
        });
    }

    // 2. Monthly Expense Chart
    const expCtx = document.getElementById('monthlyExpenseChart')?.getContext('2d');
    if (expCtx) {
        new Chart(expCtx, {
            type: 'line',
            data: {
                labels: data.months,
                datasets: [{
                    label: 'Expenses (INR)',
                    data: data.monthly_expenses,
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.15)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#EF4444'
                }]
            },
            options: baseChartOptions
        });
    }

    // 3. Monthly Profit Chart
    const profCtx = document.getElementById('monthlyProfitChart')?.getContext('2d');
    if (profCtx) {
        new Chart(profCtx, {
            type: 'bar',
            data: {
                labels: data.months,
                datasets: [{
                    label: 'Net Profit (INR)',
                    data: data.monthly_profit,
                    backgroundColor: data.monthly_profit.map(v => v >= 0 ? '#10B981' : '#EF4444'),
                    borderRadius: 6
                }]
            },
            options: baseChartOptions
        });
    }
}

// 4, 5: Vehicle-wise Revenue & Expense
function initVehicleCharts(data) {
    const vehRevCtx = document.getElementById('vehicleRevenueChart')?.getContext('2d');
    if (vehRevCtx) {
        new Chart(vehRevCtx, {
            type: 'bar',
            data: {
                labels: data.vehicles.labels,
                datasets: [{
                    label: 'Freight Revenue',
                    data: data.vehicles.revenue,
                    backgroundColor: '#06B6D4',
                    borderRadius: 6
                }]
            },
            options: baseChartOptions
        });
    }

    const vehExpCtx = document.getElementById('vehicleExpenseChart')?.getContext('2d');
    if (vehExpCtx) {
        new Chart(vehExpCtx, {
            type: 'bar',
            data: {
                labels: data.vehicles.labels,
                datasets: [{
                    label: 'Vehicle Operating Cost',
                    data: data.vehicles.expenses,
                    backgroundColor: '#F59E0B',
                    borderRadius: 6
                }]
            },
            options: baseChartOptions
        });
    }
}

// 6, 7: Driver Performance & Fuel Consumption
function initDriverAndFuelCharts(data) {
    // 6. Driver-wise Performance
    const drvCtx = document.getElementById('driverPerformanceChart')?.getContext('2d');
    if (drvCtx) {
        new Chart(drvCtx, {
            type: 'bar',
            data: {
                labels: data.drivers.labels,
                datasets: [
                    {
                        label: 'Trips Completed',
                        data: data.drivers.trips,
                        backgroundColor: '#8B5CF6',
                        yAxisID: 'yTrips',
                        borderRadius: 6
                    },
                    {
                        label: 'Revenue (₹)',
                        data: data.drivers.revenue,
                        backgroundColor: 'rgba(59, 130, 246, 0.4)',
                        borderColor: '#3B82F6',
                        type: 'line',
                        yAxisID: 'y'
                    }
                ]
            },
            options: {
                ...baseChartOptions,
                scales: {
                    ...baseChartOptions.scales,
                    yTrips: {
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#8B5CF6', stepSize: 1 }
                    }
                }
            }
        });
    }

    // 7. Fuel Consumption Analysis (Expected vs Actual Liters)
    const fuelCtx = document.getElementById('fuelConsumptionChart')?.getContext('2d');
    if (fuelCtx) {
        new Chart(fuelCtx, {
            type: 'bar',
            data: {
                labels: data.fuel_analysis.labels,
                datasets: [
                    {
                        label: 'Expected Fuel (L)',
                        data: data.fuel_analysis.expected,
                        backgroundColor: '#3B82F6',
                        borderRadius: 5
                    },
                    {
                        label: 'Actual Fuel (L)',
                        data: data.fuel_analysis.actual,
                        backgroundColor: '#F97316',
                        borderRadius: 5
                    }
                ]
            },
            options: {
                ...baseChartOptions,
                scales: {
                    ...baseChartOptions.scales,
                    y: {
                        ticks: {
                            color: '#64748B',
                            callback: function(v) { return v + ' L'; }
                        }
                    }
                }
            }
        });
    }
}

// 8. Profit vs Expense Comparison (Doughnut / Pie)
function initProfitExpenseComparison(data) {
    const pieCtx = document.getElementById('profitExpensePieChart')?.getContext('2d');
    if (pieCtx) {
        new Chart(pieCtx, {
            type: 'doughnut',
            data: {
                labels: ['Operating Expenses', 'Net Fleet Profit', 'Trip Losses'],
                datasets: [{
                    data: [data.totals.expenses, data.totals.profit, data.totals.loss],
                    backgroundColor: ['#F59E0B', '#10B981', '#EF4444'],
                    borderColor: '#111B31',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(ctx) {
                                return ctx.label + ': ₹' + Number(ctx.raw).toLocaleString('en-IN');
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
}
