// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#e74c3c';
                } else {
                    input.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill all required fields!');
            }
        });
    });

    // Load diseases when crop is selected
    const cropSelect = document.getElementById('crop_id');
    if (cropSelect) {
        cropSelect.addEventListener('change', loadDiseases);
    }
});

// Function to load diseases by crop
function loadDiseases() {
    const cropId = document.getElementById('crop_id').value;
    const diseaseSelect = document.getElementById('disease_id');
    
    if (!diseaseSelect) return;
    
    if (cropId) {
        fetch(`/api/diseases/${cropId}`)
            .then(response => response.json())
            .then(data => {
                diseaseSelect.innerHTML = '<option value="">-- Select disease --</option>';
                if (data.length === 0) {
                    diseaseSelect.innerHTML += '<option disabled>No diseases found</option>';
                } else {
                    data.forEach(disease => {
                        const option = document.createElement('option');
                        option.value = disease.id;
                        option.textContent = disease.name;
                        diseaseSelect.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error loading diseases:', error));
    } else {
        diseaseSelect.innerHTML = '<option value="">-- Select disease --</option>';
    }
}

// Clear form on reset
function clearForm() {
    document.querySelectorAll('input, select, textarea').forEach(el => {
        el.style.borderColor = '';
    });
}

// Add success message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert-success');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});