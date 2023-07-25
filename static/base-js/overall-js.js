const csrfToken = window.csrfToken;

function copyToClipboard(text) {
    const tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    alert('URL copied to clipboard: ' + text); // Show a confirmation message or any other desired action
}

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
                'X-CSRFToken': csrfToken,
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
// JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(likeButton => {
        likeButton.addEventListener('click', async (event) => {
            event.preventDefault();

            // Get the post ID and action from the data attributes
            const postId = likeButton.closest('.like-container').dataset.postId;
            const action = likeButton.dataset.action;

            // Trigger the AJAX request to like or dislike the post
            const response = await fetch(`/like_post/${postId}/${action}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Toggle the heart icon's classes and fill attribute based on the like status
                const heartIcon = likeButton.querySelector(`#heart-icon${postId}`);

                if (action === 'like') {
                    heartIcon.setAttribute('fill', 'red');
                    likeButton.dataset.action = 'dislike';
                } else if (action === 'dislike') {
                    heartIcon.setAttribute('fill', 'black');
                    likeButton.dataset.action = 'like';
                }

                // Update the like count if needed
                const likeCountElement = document.querySelector(`#numLike${postId}`);
                const likeCount = parseInt(likeCountElement.textContent);
                if (action === 'like') {
                    likeCountElement.textContent = likeCount + 1;
                } else if (action === 'dislike') {
                    likeCountElement.textContent = likeCount - 1;
                }
            } else {
                console.error('Error liking/disliking post:', response.status);
            }
        });
    });
});
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
                    'X-CSRFToken': csrfToken,
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

document.addEventListener('DOMContentLoaded', () => {
    const commentInput = document.getElementById('commentInput');
    const postCommentButton = document.getElementById('postCommentButton');
    const commentsContainer = document.getElementById('commentsContainer');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    async function addComment(comment) {
        const postId = commentsContainer.dataset.postId;
        const url = `comment/`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ comment: comment })
        });

        if (response.ok) {
            const data = await response.json();
            const newComment = document.createElement('div');
            const profileName = `${data.user.profile.first_name} ${data.user.profile.last_name}` || data.user.username;
            const profileImage = data.user.profile.image || "{% static 'images/person.png' %}";
            newComment.innerHTML = `
                <div class="comments" id="comment${data.comment_id}">
                    <div class="top">
                        <div class="userDetails">
                            <div class="comment-data">
                                <div class="profilepic">
                                    <div class="profile_img">
                                        <div class="image">
                                            <!-- User Profile Image -->
                                            <a href="/profile/${data.user.username}">
                                                <img src="${profileImage}" alt="Profile Image">
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                <p>
                                    <!-- Link to User Profile Details Page -->
                                    <a href="/profile/${data.user.username}" style="font-weight: bold;">
                                        ${profileName}
                                    </a>
                                    <!-- User Comment -->
                                    ${data.comment}
                                </p>
                            </div>
                            <span>${data.timestamp}</span>
                        </div>
                    </div>
                </div>
            `;
            commentsContainer.appendChild(newComment);
            commentInput.value = ''; // Clear the textarea after posting the comment
        } else {
            console.error('Error adding comment:', response.status);
        }
    }

    postCommentButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default form submission behavior
        const comment = commentInput.value.trim();
        if (comment !== '') {
            addComment(comment);
        }
    });
});