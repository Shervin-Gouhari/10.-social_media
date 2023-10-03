let topComments = document.getElementById("topComments");
let newestComments = document.getElementById("newestComments");
const orderBy = function (by, postSlug) {
    axios
        .get(`/post/detail/${postSlug}/API`, { params: { by: by } })
        .then((res) => {
            if (res.data.response != undefined) {
                commentContainer.innerHTML = res.data.response;
                commentLikeListener();
            } else {
                console.log("error");
            }
        })
        .catch((err) => {
            console.log(err);
        });
};

topComments.addEventListener("click", (e) => {
    orderBy("comments_orderByLikesAscending", topComments.getAttribute("post-slug"));
});
newestComments.addEventListener("click", (e) => {
    orderBy("comments_orderByCreationAscending", newestComments.getAttribute("post-slug"));
});
