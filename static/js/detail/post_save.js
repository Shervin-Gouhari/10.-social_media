let postSaveButton = document.querySelector("a.signet");
postSaveButton.addEventListener("click", (e) => {
    if (requestUserId != "None") {
        var fd = new FormData();
        fd.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
        fd.append("post_id", postSaveButton.getAttribute("data-postId"));
        let action;
        if (postSaveButton.firstElementChild.classList.contains("fa-solid")) {
            action = "unsave";
        } else {
            action = "save";
        }
        fd.append("post_action", action);
        axios
            .post("/post/post-save/", fd)
            .then((res) => {
                if (action == "save") {
                    postSaveButton.firstElementChild.classList.replace("fa-regular", "fa-solid");
                } else {
                    postSaveButton.firstElementChild.classList.replace("fa-solid", "fa-regular");
                }
            })
            .catch((err) => {
                console.log(err);
            });
    } else {
        alert("You have to login first before saving.");
    }
});
