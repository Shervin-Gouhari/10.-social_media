let savedButton = document.getElementById("SAVED-button");
let postsButton = document.getElementById("POSTS-button");
let taggedButton = document.getElementById("TAGGED-button");
savedButton.addEventListener("click", (e) => {
    if (savedButton.classList.contains("active")) {
    } else {
        savedButton.classList.add("active");
        postsButton.classList.remove("active");
        taggedButton.classList.remove("active");
        axios
            .get("", {
                params: { arrangement: "SAVED", page: 1 },
            })
            .then((res) => {
                if (res.data.response !== "failure") {
                    gallery.innerHTML = res.data.response;
                }
                if (res.data.next_response === false) {
                    loadMoreButton.classList.add("display-none");
                } else {
                    loadMoreButton.classList.remove("display-none");
                    postsPage = 1;
                    savedPage = 1;
                    taggedPage = 1;
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }
});
