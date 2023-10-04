let gallery = document.getElementById("gallery");
let loadMoreButton = document.getElementById("load-more-button");
let postsPage = 1;
let savedPage = 1;
let taggedPage = 1;

loadMoreButton.addEventListener("click", (e) => {
    if (savedButton.classList.contains("active")) {
        var params = { arrangement: "SAVED", page: (savedPage += 1) };
    } else if (taggedButton.classList.contains("active")) {
        var params = { arrangement: "TAGGED", page: (taggedPage += 1) };
    } else {
        var params = { arrangement: "POSTS", page: (postsPage += 1) };
    }

    axios
        .get("", {
            params: params,
        })
        .then((res) => {
            if (res.data.response !== "failure") {
                gallery.innerHTML += res.data.response;
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
});
