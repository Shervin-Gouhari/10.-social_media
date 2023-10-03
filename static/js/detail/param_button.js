let paramButton = document.getElementById("param-button");
let paramContainer = document.getElementById("param-container");
paramButton.addEventListener("click", (e) => {
    if (requestUserId != "None") {
        paramContainer.classList.toggle("display-none");
    } else {
        alert("You have to login first.");
    }
});
document.addEventListener("click", (e) => {
    if (!paramButton.contains(e.target) && !paramContainer.contains(e.target)) {
        paramContainer.classList.add("display-none");
    }
});
