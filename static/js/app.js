// Mental Health Fitness Tracker - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');

    // Form submission handler
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const file1 = document.getElementById('file1').files[0];
        const file2 = document.getElementById('file2').files[0];
        
        if (!file1 || !file2) {
            showError('Please select both CSV files');
            return;
        }
        
        formData.append('file1', file1);
        formData.append('file2', file2);
        
        // Show loading state
        showLoading();
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                displayResults(result.data);
            } else {
                showError(result.error || 'An error occurred while processing the files');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            hideLoading();
        }
    });

    function showLoading() {
        loadingSpinner.style.display = 'block';
        resultsSection.style.display = 'none';
        errorAlert.style.display = 'none';
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }

    function hideLoading() {
        loadingSpinner.style.display = 'none';
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-chart-line me-2"></i>Analyze Data';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.style.display = 'block';
        resultsSection.style.display = 'none';
    }

    function displayResults(data) {
        // Hide error alert
        errorAlert.style.display = 'none';
        
        // Display statistics
        displayStatistics(data.statistics);
        
        // Display model metrics
        displayModelMetrics(data.model_metrics);
        
        // Display visualizations
        displayVisualizations(data.visualizations);
        
        // Show results section with animation
        resultsSection.style.display = 'block';
        resultsSection.classList.add('fade-in-up');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function displayStatistics(stats) {
        const statisticsCards = document.getElementById('statisticsCards');
        
        const cards = [
            {
                title: 'Total Records',
                value: stats.shape[0].toLocaleString(),
                icon: 'fas fa-database',
                color: 'bg-primary'
            },
            {
                title: 'Features',
                value: stats.shape[1],
                icon: 'fas fa-list',
                color: 'bg-info'
            },
            {
                title: 'Mean Mental Fitness',
                value: stats.mean_mental_fitness.toFixed(4),
                icon: 'fas fa-chart-line',
                color: 'bg-success'
            },
            {
                title: 'Std Deviation',
                value: stats.std_mental_fitness.toFixed(4),
                icon: 'fas fa-chart-bar',
                color: 'bg-warning'
            },
            {
                title: 'Min Value',
                value: stats.min_mental_fitness.toFixed(4),
                icon: 'fas fa-arrow-down',
                color: 'bg-danger'
            },
            {
                title: 'Max Value',
                value: stats.max_mental_fitness.toFixed(4),
                icon: 'fas fa-arrow-up',
                color: 'bg-secondary'
            }
        ];
        
        statisticsCards.innerHTML = cards.map(card => `
            <div class="col-md-4 col-lg-2 mb-3">
                <div class="stat-card ${card.color}">
                    <i class="${card.icon} fa-2x mb-2"></i>
                    <div class="stat-value">${card.value}</div>
                    <div class="stat-label">${card.title}</div>
                </div>
            </div>
        `).join('');
    }

    function displayModelMetrics(metrics) {
        const modelMetrics = document.getElementById('modelMetrics');
        
        const trainMetrics = [
            { title: 'Training MSE', value: metrics.train.mse.toFixed(6), color: 'text-primary' },
            { title: 'Training RMSE', value: metrics.train.rmse.toFixed(6), color: 'text-info' },
            { title: 'Training R²', value: metrics.train.r2.toFixed(6), color: 'text-success' }
        ];
        
        const testMetrics = [
            { title: 'Testing MSE', value: metrics.test.mse.toFixed(6), color: 'text-primary' },
            { title: 'Testing RMSE', value: metrics.test.rmse.toFixed(6), color: 'text-info' },
            { title: 'Testing R²', value: metrics.test.r2.toFixed(6), color: 'text-success' }
        ];
        
        modelMetrics.innerHTML = `
            <div class="col-md-6">
                <div class="metric-card">
                    <h5 class="metric-title text-primary">
                        <i class="fas fa-graduation-cap me-2"></i>
                        Training Performance
                    </h5>
                    ${trainMetrics.map(metric => `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span>${metric.title}:</span>
                            <span class="${metric.color} fw-bold">${metric.value}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="col-md-6">
                <div class="metric-card">
                    <h5 class="metric-title text-success">
                        <i class="fas fa-test-tube me-2"></i>
                        Testing Performance
                    </h5>
                    ${testMetrics.map(metric => `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span>${metric.title}:</span>
                            <span class="${metric.color} fw-bold">${metric.value}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    function displayVisualizations(visualizations) {
        // Display correlation heatmap
        displayVisualization('correlationHeatmap', visualizations.correlation_heatmap, 'Correlation heatmap could not be generated');
        
        // Display pairplot
        displayVisualization('pairplot', visualizations.pairplot, 'Pairplot could not be generated');
        
        // Display distribution histogram
        displayVisualization('distributionHistogram', visualizations.distribution_histogram, 'Distribution analysis could not be generated');
        
        // Display time series analysis
        displayVisualization('timeSeriesAnalysis', visualizations.time_series_analysis, 'Time series analysis could not be generated');
        
        // Display feature importance
        displayVisualization('featureImportance', visualizations.feature_importance, 'Feature importance analysis could not be generated');
    }

    function displayVisualization(elementId, imageData, errorMessage) {
        const imgElement = document.getElementById(elementId);
        if (imageData) {
            imgElement.src = `data:image/png;base64,${imageData}`;
            imgElement.alt = elementId.replace(/([A-Z])/g, ' $1').trim();
            imgElement.style.display = 'block';
            imgElement.parentElement.parentElement.style.display = 'block';
        } else {
            imgElement.style.display = 'none';
            imgElement.parentElement.innerHTML = `<p class="text-muted text-center"><i class="fas fa-exclamation-circle me-2"></i>${errorMessage}</p>`;
        }
    }

    // File input validation
    document.getElementById('file1').addEventListener('change', function(e) {
        validateFile(e.target, 'Mental disorders data');
    });
    
    document.getElementById('file2').addEventListener('change', function(e) {
        validateFile(e.target, 'Substance use data');
    });

    function validateFile(input, fileType) {
        const file = input.files[0];
        if (file) {
            if (!file.name.toLowerCase().endsWith('.csv')) {
                showError(`${fileType} must be a CSV file`);
                input.value = '';
                return;
            }
            
            if (file.size > 16 * 1024 * 1024) { // 16MB limit
                showError(`${fileType} file is too large. Maximum size is 16MB`);
                input.value = '';
                return;
            }
            
            // Clear any previous errors
            errorAlert.style.display = 'none';
        }
    }

    // Add smooth scrolling for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });
});
