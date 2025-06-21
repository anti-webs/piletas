// Client-side JavaScript for Ferreira Quintas Piscinas

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Password strength indicator for registration form
    const passwordField = document.getElementById('password');
    const strengthIndicator = document.getElementById('password-strength');
    
    if (passwordField && strengthIndicator) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 6) strength += 1;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 1;
            if (password.match(/\d/)) strength += 1;
            if (password.match(/[^a-zA-Z\d]/)) strength += 1;
            
            // Update strength indicator
            if (strength === 0) {
                strengthIndicator.textContent = '';
                strengthIndicator.className = '';
            } else if (strength <= 2) {
                strengthIndicator.textContent = 'Débil';
                strengthIndicator.className = 'text-danger';
            } else if (strength === 3) {
                strengthIndicator.textContent = 'Media';
                strengthIndicator.className = 'text-warning';
            } else {
                strengthIndicator.textContent = 'Fuerte';
                strengthIndicator.className = 'text-success';
            }
        });
    }

    // Confirm password check
    const confirmPasswordField = document.getElementById('confirm_password');
    const passwordMatchIndicator = document.getElementById('password-match');
    
    if (passwordField && confirmPasswordField && passwordMatchIndicator) {
        confirmPasswordField.addEventListener('input', function() {
            if (this.value === passwordField.value) {
                passwordMatchIndicator.textContent = 'Las contraseñas coinciden';
                passwordMatchIndicator.className = 'text-success';
            } else {
                passwordMatchIndicator.textContent = 'Las contraseñas no coinciden';
                passwordMatchIndicator.className = 'text-danger';
            }
        });
    }

    // Handle pool selection in service request form
    const poolSelector = document.querySelectorAll('.select-pool-btn');
    
    poolSelector.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const poolId = this.getAttribute('data-pool-id');
            const poolName = this.getAttribute('data-pool-name');
            
            // Set the pool ID in the form
            document.getElementById('pool_id').value = poolId;
            
            // Update the UI to show selected pool
            const selectedPoolDisplay = document.getElementById('selected-pool');
            if (selectedPoolDisplay) {
                selectedPoolDisplay.textContent = poolName;
                selectedPoolDisplay.parentElement.classList.remove('d-none');
            }
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
