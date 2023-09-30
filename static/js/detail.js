// Slider
let previousSlider = document.getElementById("previous-slider");
let nextSlider = document.getElementById("next-slider");
let medias = document.querySelector(".post__medias");
let postIndicators = document.getElementsByClassName("post__indicators");
let index = 0;
previousSlider.addEventListener("click", (e) => {
    medias.scrollLeft -= 800;
    if (index == medias.children.length - 1) {
        nextSlider.classList.toggle("hide");
    }
    if (index == 1) {
        previousSlider.classList.toggle("hide");
    }
    if (index - 2 == 1) {
        previousSlider.classList.toggle("hide");
    }
    postIndicators[0].children[index].classList.toggle("post__indicator--active");
    index -= 1;
    postIndicators[0].children[index].classList.toggle("post__indicator--active");
});
nextSlider.addEventListener("click", (e) => {
    medias.scrollLeft += 800;
    if (index == 0) {
        previousSlider.classList.toggle("hide");
    }
    if (index + 2 == medias.children.length) {
        nextSlider.classList.toggle("hide");
    }
    postIndicators[0].children[index].classList.toggle("post__indicator--active");
    index += 1;
    postIndicators[0].children[index].classList.toggle("post__indicator--active");
});
