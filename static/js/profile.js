// Create Posts
let postPopUpButton = document.getElementsByClassName("btn profile-settings-btn")[0];
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

// Load More Posts
let gallery = document.getElementsByClassName("gallery")[0];
let blockRequest = false;
let page = 1;
window.addEventListener("scroll", (e) => {
    let innerHeight = window.innerHeight;
    let pageYOffset = window.pageYOffset;
    let clientHeight = document.body.clientHeight;
    let galleryItem = document.getElementsByClassName("gallery-item");
    if (innerHeight + pageYOffset >= clientHeight && blockRequest == false) {
        blockRequest = true;
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
                        for (let item of galleryItem) {
                            if (item.classList.contains("animate__fadeInUp")) {
                                item.classList.remove("animate__fadeInUp");
                            }
                        }
                    }, 1000);
                    blockRequest = false;
                }
            })
            .catch((err) => {
                console.log(err);
                blockRequest = false;
            });
    }
});
