document.addEventListener('DOMContentLoaded', () => {
    const commentInput = document.getElementById('commentInput');
    const postCommentButton = document.getElementById('postCommentButton');
    const commentsContainer = document.getElementById('commentsContainer');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    async function addComment(comment) {
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
                            <span>now</span>
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