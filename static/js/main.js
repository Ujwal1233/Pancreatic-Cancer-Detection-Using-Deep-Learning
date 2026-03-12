document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('image-input');
    const previewImage = document.getElementById('preview-image');
    const processingSteps = document.getElementById('processing-steps');
    const resultSection = document.getElementById('result-section');
    const loadingSpinner = document.getElementById('loading-spinner');
    const downloadButton = document.getElementById('download-report'); // Button for report download

    // Create a Bootstrap alert container
    const alertContainer = document.createElement('div');
    alertContainer.id = 'alert-container';
    alertContainer.className = 'mt-3';
    uploadForm.parentNode.insertBefore(alertContainer, uploadForm);

    // Function to show alert messages
    function showAlert(message, type = 'danger') {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }

    // ==========================
    // IMAGE UPLOAD AND ANALYSIS
    // ==========================
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            if (!fileInput.files[0]) {
                showAlert('⚠️ Please select an image before analyzing.', 'warning');
                return;
            }
            
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            
            try {
                loadingSpinner.classList.remove('d-none');
                resultSection.classList.add('d-none');
                showAlert('', ''); // Clear any existing alert
                
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                // 🔒 SAFETY CHECK
                const contentType = response.headers.get("content-type");
                
                if (!contentType || !contentType.includes("application/json")) {
                    throw new Error("Session expired or server error. Please log in again.");
                }
                
                const data = await response.json();
                
                if (!response.ok || data.error) {
                    throw new Error(data.error || "An unexpected error occurred.");
                }

                
                // Display processing steps
                processingSteps.innerHTML = '';
                Object.entries(data.processed_images).forEach(([step, imageData]) => {
                    const stepDiv = document.createElement('div');
                    stepDiv.className = 'col-md-6 mb-4';
                    stepDiv.innerHTML = `
                        <div class="card shadow">
                            <img src="${imageData}" class="card-img-top" alt="${step}">
                            <div class="card-body text-center">
                                <h5 class="card-title text-capitalize">${step}</h5>
                            </div>
                        </div>
                    `;
                    processingSteps.appendChild(stepDiv);
                });
                
                // Display results
                document.getElementById('cancer-type').textContent = data.cancer_type;
                document.getElementById('cancer-stage').textContent = data.cancer_stage;
                document.getElementById('confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
                
                resultSection.classList.remove('d-none');
                showAlert('✅ Image successfully analyzed!', 'success');
            } catch (error) {
                // Show styled alert for errors
                showAlert('❌ ' + error.message, 'danger');
            } finally {
                loadingSpinner.classList.add('d-none');
            }
        });
    }

    // ==========================
    // IMAGE PREVIEW
    // ==========================
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ==========================
    // DOWNLOAD HEALTH REPORT
    // ==========================
    if (downloadButton) {
        downloadButton.addEventListener('click', async () => {
            const cancerType = document.getElementById('cancer-type').textContent || 'N/A';
            const cancerStage = document.getElementById('cancer-stage').textContent || 'N/A';
            const confidenceText = document.getElementById('confidence').textContent || '0%';
            const confidence = parseFloat(confidenceText.replace('%', '')) / 100;

            try {
                const response = await fetch('/download_report', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    headers: {
                    'Content-Type': 'application/json'
                    },  
                    body: JSON.stringify({
                        cancer_type: cancerType,
                        cancer_stage: cancerStage,
                        confidence: confidence
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = "Health_Report.pdf";
                    link.click();
                    showAlert("✅ Health Report downloaded successfully!", "success");
                } else {
                    showAlert("❌ Failed to generate report. Please try again.", "danger");
                }
            } catch (error) {
                showAlert("⚠️ Error generating report: " + error.message, "danger");
            }
        });
    }
});
