// Profile Container
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

// Actions Container
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

// Search Container
let searchBar = document.getElementById("search-bar");
let searchContainer = document.querySelector("div.search-container");
["keyup", "paste"].forEach((event) =>
    searchBar.addEventListener(event, (e) => {
        searchContainer.classList.remove("display-none");
        searchContainer.innerText = "Searching...";
        let searchQuery = e.target.value;
        axios
            .get("/account/search/", {
                params: {
                    query: searchQuery,
                },
            })
            .then((res) => {
                if (res.data.response !== "failure") {
                    searchContainer.innerHTML = res.data.response;
                } else {
                    searchContainer.classList.add("display-none");
                }
            })
            .catch((err) => {
                console.log(err);
            });
    })
);
document.addEventListener("click", (e) => {
    if (e.target != searchBar && !searchContainer.contains(e.target)) {
        searchContainer.classList.add("display-none");
    }
});
