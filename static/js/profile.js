// Load More Posts
let gallery = document.getElementById("gallery");
let loadMoreButton = document.getElementById("load-more-button");
let page = 1;
loadMoreButton.addEventListener("click", (e) => {
    let galleryItems = document.getElementsByClassName("gallery-item");
    page += 1;
    axios
        .get("", {
            params: {
                page: page,
            },
        })
        .then((res) => {
            if (res.data.response !== "failure") {
                gallery.innerHTML += res.data.response;
                window.setInterval(() => {
                    for (let item of galleryItems) {
                        if (item.classList.contains("animate__fadeInUp")) {
                            item.classList.remove("animate__fadeInUp");
                        }
                    }
                }, 1000);
            }
            if (res.data.next_response === "failure") {
                loadMoreButton.remove();
            }
        })
        .catch((err) => {
            console.log(err);
        });
});

// Create Posts
let postPopUpButton = document.getElementById("post-pop-up-button");
postPopUpButton.addEventListener("click", (e) => {
    axios
        .get("/post/create/")
        .then((res) => {
            Swal.fire({
                width: 700,
                title: "Create Your Post",
                html: res.data.response,
                showConfirmButton: false,
            });
        })
        .catch((err) => {
            console.log(err);
        });
});
