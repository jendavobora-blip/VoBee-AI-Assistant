// Waitlist form submission handler

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('waitlist-form');
    const responseMessage = document.getElementById('response-message');
    const submitBtn = form.querySelector('.submit-btn');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = {
            email: document.getElementById('email').value,
            use_case: document.getElementById('use_case').value,
            persona: document.getElementById('persona').value
        };

        // Validate form
        if (!formData.email || !formData.use_case || !formData.persona) {
            showMessage('Please fill in all required fields', 'error');
            return;
        }

        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.textContent = 'Joining...';

        try {
            // Submit to API
            const response = await fetch('/api/waitlist/join', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                // Success
                showMessage(
                    `Success! You're #${data.position} in line out of ${data.total_waiting} people waiting. ` +
                    `Estimated wait time: ${data.estimated_wait}. We'll email you when it's your turn!`,
                    'success'
                );
                form.reset();
            } else {
                // Error
                showMessage(data.error || 'Failed to join waitlist. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Network error. Please check your connection and try again.', 'error');
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Join Waitlist';
        }
    });

    function showMessage(message, type) {
        responseMessage.textContent = message;
        responseMessage.className = `response-message ${type}`;
        responseMessage.style.display = 'block';

        // Scroll to message
        responseMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Hide success message after 10 seconds
        if (type === 'success') {
            setTimeout(() => {
                responseMessage.style.display = 'none';
            }, 10000);
        }
    }
});
