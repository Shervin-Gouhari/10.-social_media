const commentLikeListener = function () {
    let commentLikeButton = document.getElementsByClassName("comment-like");
    Array.from(commentLikeButton).forEach((cm, i) => {
        cm.addEventListener("click", (e) => {
            if (requestUserId != "None") {
                let commentId = cm.getAttribute("data-commentId");
                let commentAction = cm.getAttribute("data-commentAction");
                let commentLikeIcon = cm.firstElementChild;
                let commentLikeNumber = document.getElementsByClassName("comment-likes")[i].firstElementChild;
                let commentLikeOrLikes = commentLikeNumber.nextElementSibling;
                var fd = new FormData();
                fd.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
                fd.append("comment_id", commentId);
                fd.append("comment_action", commentAction);
                axios
                    .post("/post/comment-like/", fd)
                    .then((res) => {
                        if (commentAction == "like") {
                            commentLikeIcon.classList = "fas fa-heart heart-active";
                            cm.setAttribute("data-commentAction", "dislike");
                            commentLikeNumber.innerText = parseInt(commentLikeNumber.innerText) + 1;
                            if (parseInt(commentLikeNumber.innerText) > 1) {
                                commentLikeOrLikes.innerText = "Likes";
                            }
                        } else {
                            commentLikeIcon.classList = "far fa-heart";
                            cm.setAttribute("data-commentAction", "like");
                            commentLikeNumber.innerText = parseInt(commentLikeNumber.innerText) - 1;
                            if (parseInt(commentLikeNumber.innerText) < 2) {
                                commentLikeOrLikes.innerText = "Like";
                            }
                        }
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            } else {
                alert("You have to login first before liking.");
            }
        });
    });
};
commentLikeListener();
