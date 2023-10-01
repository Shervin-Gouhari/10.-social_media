let heart = document.querySelector(".heart");
let actionsContainer = document.getElementsByClassName("actions-container")[0];
document.addEventListener("click", (e) => {
    if (
        !e.target.classList.contains("fa-heart") &&
        !e.target.classList.contains("actions-container") &&
        actionsContainer.classList.contains("show-box")
    ) {
        actionsContainer.classList.remove("show-box");
        heart.innerHTML = '<i class="fa-regular fa-heart"></i>';
    }
});
heart.addEventListener("click", (e) => {
    actionsContainer.classList.toggle("show-box");
});
