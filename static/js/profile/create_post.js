let postPopUpButton1 = document.getElementById("post-pop-up-button1");
let postPopUpButton2 = document.getElementById("post-pop-up-button2");
[postPopUpButton1, postPopUpButton2].forEach((event) => {
    event.addEventListener("click", (e) => {
        e.preventDefault();
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
});
