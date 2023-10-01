let profileModalContainer = document.getElementsByClassName("profile-modal-container")[0];
let profile = document.getElementsByClassName("profile")[0];

profile.addEventListener("click", () => {
    profileModalContainer.classList.toggle("display-none");
});
document.addEventListener("click", (e) => {
    if (!e.target.classList.contains("profile-box")) {
        profileModalContainer.classList.add("display-none");
    }
});
