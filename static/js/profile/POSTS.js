postsButton.addEventListener("click", (e) => {
    if (postsButton.classList.contains("active")) {
    } else {
        postsButton.classList.add("active");
        savedButton.classList.remove("active");
        taggedButton.classList.remove("active");
        axios
            .get("", {
                params: { arrangement: "POSTS", page: 1 },
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
