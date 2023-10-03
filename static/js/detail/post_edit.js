let postEditButton = document.getElementById("post-edit-button");

const swalPostUpdate = function (message) {
    Swal.fire({
        position: "center",
        background: "black",
        showConfirmButton: false,
        showCancelButton: true,
        html: message,
    });
};

postEditButton.addEventListener("click", (e) => {
    e.preventDefault();
    axios
        .get(postEditButton.getAttribute("href"))
        .then((res) => {
            swalPostUpdate(res.data.response);
        })
        .catch((err) => {
            console.log(err);
        });
});
