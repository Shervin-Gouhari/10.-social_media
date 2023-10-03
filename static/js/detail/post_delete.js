let postDeleteButton = document.getElementById("post-delete-button");

const swalPostDelete = function (message) {
    Swal.fire({
        position: "center",
        icon: "error",
        background: "black",
        showConfirmButton: false,
        showCancelButton: true,
        html: message,
    });
};

postDeleteButton.addEventListener("click", (e) => {
    e.preventDefault();
    axios
        .get(postDeleteButton.getAttribute("href"))
        .then((res) => {
            swalPostDelete(res.data.response);
        })
        .catch((err) => {
            console.log(err);
        });
});
