let messages = document.getElementsByClassName("messages");
Array.from(messages).forEach((e) => {
    if (e.innerText.includes("You must wait")) {
        setInterval(() => {
            let num = e.innerText.match(/\d+/g);
            if (num > 0) {
                e.innerText = `You must wait "${num - 1}" seconds before retrying.`;
            } else location.reload();
        }, 1000);
    }
});
