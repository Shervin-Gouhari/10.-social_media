let commentPostButton = document.getElementById("comment-post-button");
let commentTextForm = document.getElementById("comment-text-form");
let commentContainer = document.getElementById("comment-container");
let comments = document.getElementsByClassName("comments");
let numberOfComments = document.querySelector("#numberOfComments > div");

commentPostButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (requestUserId != "None") {
        fd = new FormData();
        fd.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
        fd.append("text", commentTextForm.value);
        axios
            .post("", fd)
            .then((res) => {
                if (res.data.response != undefined) {
                    let newComment = res.data.response;
                    commentContainer.innerHTML = newComment + commentContainer.innerHTML;
                    commentTextForm.value = "";
                    if (numberOfComments != undefined) {
                        numberOfComments.innerText = parseInt(numberOfComments.innerText) + 1;
                    }
                    commentLikeListener();
                    window.setInterval(() => {
                        for (let item of comments) {
                            if (item.classList.contains("animate__fadeInDown")) {
                                item.classList.remove("animate__fadeInDown");
                            }
                        }
                    }, 1000);
                } else {
                    console.log("error");
                }
            })
            .catch((err) => {
                console.log(err);
            });
    } else {
        alert("You have to login first before commenting.");
    }
});
