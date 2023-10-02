const swalFollowing = function (html) {
    Swal.fire({
        position: "center",
        background: "black",
        html: html,
        showConfirmButton: false,
    });
};

let followingButton = document.getElementById("following-button");
let followersButton = document.getElementById("followers-button");
[followingButton, followersButton].forEach((event) => {
    event.addEventListener("click", (e) => {
        axios
            .get(`/account/profile/${user}/${event.innerText.trim()}`)
            .then((res) => {
                let response = res.data.response;
                swalFollowing(response);
            })
            .catch((err) => {
                console.log(err);
            });
    });
});
