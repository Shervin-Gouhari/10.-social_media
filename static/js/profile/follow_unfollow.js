let userFollowButton = document.getElementById("follow-btn");
let userAction = userFollowButton.getAttribute("data-userAction");
let followersCounter = document.getElementById("followers-counter");

userFollowButton.addEventListener("click", (e) => {
    e.preventDefault();
    var fd = new FormData();
    fd.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
    fd.append("user_id", userFollowButton.getAttribute("data-userId"));
    fd.append("user_action", userAction);
    axios
        .post("/account/follow/", fd)
        .then((res) => {
            if (userAction === "follow") {
                userAction = "unfollow";
                userFollowButton.innerText = "Unfollow";
                followersCounter.innerText = parseInt(followersCounter.innerText) + 1;
            } else {
                userAction = "follow";
                userFollowButton.innerText = "Follow";
                followersCounter.innerText = parseInt(followersCounter.innerText) - 1;
            }
        })
        .catch((err) => {
            console.log(err);
        });
});
