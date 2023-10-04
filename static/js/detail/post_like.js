let requestUserId = document.getElementById("request-user-id").innerText;

let postLikeButton = document.querySelector("a.like");
let postLikeNumber = document.getElementById("like-number");
let postLikeOrLikes = document.getElementById("like-or-likes");

postLikeButton.addEventListener("click", (e) => {
    if (requestUserId != "None") {
        var fd = new FormData();
        fd.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
        fd.append("post_id", postLikeButton.getAttribute("data-postId"));
        let action;
        if (postLikeButton.firstElementChild.classList.contains("fa-solid")) {
            action = "dislike";
        } else {
            action = "like";
        }
        fd.append("post_action", action);
        axios
            .post("/post/post-like/", fd)
            .then((res) => {
                if (action == "like") {
                    postLikeButton.firstElementChild.classList.replace("fa-regular", "fa-solid");
                    postLikeNumber.innerText = parseInt(postLikeNumber.innerText) + 1;
                    if (parseInt(postLikeNumber.innerText) > 1) {
                        postLikeOrLikes.innerText = "Likes";
                    }
                } else {
                    postLikeButton.firstElementChild.classList.replace("fa-solid", "fa-regular");
                    postLikeNumber.innerText = parseInt(postLikeNumber.innerText) - 1;
                    if (parseInt(postLikeNumber.innerText) < 2) {
                        postLikeOrLikes.innerText = "Like";
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
