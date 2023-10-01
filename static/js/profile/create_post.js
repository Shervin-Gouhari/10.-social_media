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
