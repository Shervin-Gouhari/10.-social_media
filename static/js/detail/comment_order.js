let topComments = document.getElementById("topComments");
let newestComments = document.getElementById("newestComments");
const orderBy = function (by) {
    axios
        .get(`/post/detail/{{post.slug}}/API`, { params: { by: by } })
        .then((res) => {
            if (res.data.response != undefined) {
                let comments = res.data.response;
                commentContainer.innerHTML = comments;
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
    orderBy("comments_orderByLikesAscending");
});
newestComments.addEventListener("click", (e) => {
    orderBy("comments_orderByCreationAscending");
});
