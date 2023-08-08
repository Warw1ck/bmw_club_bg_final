

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
                    'X-CSRFToken': window.csrfToken,
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