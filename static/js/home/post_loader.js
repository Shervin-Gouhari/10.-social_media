let posts = document.getElementsByClassName("posts")[0];
let blockRequest = false;
let page = 1;
window.addEventListener("scroll", (e) => {
    let innerHeight = window.innerHeight;
    let pageYOffset = window.pageYOffset;
    let clientHeight = document.body.clientHeight;
    if (pageYOffset > (clientHeight * 6) / 10 && blockRequest == false) {
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
                    posts.innerHTML += res.data.response;
                    captionLoader();
                    blockRequest = false;
                }
            })
            .catch((err) => {
                console.log(err);
                blockRequest = false;
            });
    }
});
