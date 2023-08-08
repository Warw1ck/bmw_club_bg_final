
document.addEventListener('DOMContentLoaded', () => {
    const joinButtons = document.querySelectorAll('.join');

    async function handleGroupAction(button) {
        const groupId = button.dataset.groupId;
        const action = button.dataset.action;
        const details = button.dataset.details;

        let response;

        if (details === 'details') {
            response = await fetch(`${action}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.csrfToken,
                    'Content-Type': 'application/json'
                }
            });
        } else {
            response = await fetch(`/groups/${groupId}/${action}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
        }

        if (response.ok) {
            // Update the button appearance and text
            button.style.backgroundColor = action === 'join' ? 'lightskyblue' : '#A2FF86';
            button.textContent = action === 'join' ? 'Leave' : 'Join';

            // Update the data-action attribute to reflect the new state
            button.dataset.action = action === 'join' ? 'leave' : 'join';

            // Update the number of members displayed on the page
            const membersElement = document.getElementById(`members${groupId}`);
            const currentMembersCount = parseInt(membersElement.textContent);
            const newMembersCount = action === 'join' ? currentMembersCount + 1 : currentMembersCount - 1;
            membersElement.textContent = newMembersCount;
        } else {
            console.error('Error handling group action:', response.status);
        }
    }

    // Attach click event listeners to buttons
    joinButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            handleGroupAction(button);
        });
    });
});