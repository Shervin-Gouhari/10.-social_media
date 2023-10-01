const captionLoader = function () {
    let captions = document.getElementsByClassName("post-caption-main");
    let mores = document.getElementsByClassName("more-caption");
    Array.from(captions).forEach((caption, num) => {
        if (caption.getAttribute("processed") === "false") {
            let captionText = caption.innerText;
            if (captionText.trim().length > 103) {
                caption.innerText = captionText.slice(0, 100) + "...";
            } else {
                mores[num].innerText = "";
            }
            caption.setAttribute("processed", "true");
        }
    });
    Array.from(mores).forEach((more, num) => {
        more.addEventListener("click", (e) => {
            let fullCaption = captions[num].getAttribute("full-caption");
            captions[num].innerText = fullCaption;
            mores[num].innerText = "";
        });
    });
};
captionLoader();
