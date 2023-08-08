


const heartIcons = document.querySelectorAll('.notification-link');

heartIcons.forEach(icon => {
    icon.addEventListener('click', (event) => {
        event.preventDefault();

        // Get the notification ID from the data attribute
        const notificationId = icon.dataset.notificationId;
        const notificationElement = document.getElementById(`notification-${notificationId}`);

        // Trigger the AJAX request to mark the notification as read
        fetch(`/notifications/mark_read/${notificationId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.csrfToken,
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the heart icon to show as read
                    icon.querySelector('svg').classList.add('bi-heart-fill');
                    icon.querySelector('svg').classList.remove('bi-heart');

                    // Remove the notification element from the DOM
                    notificationElement.remove();
                }
            })
            .catch(error => console.error('Error marking notification as read:', error));
    });
});