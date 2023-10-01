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
