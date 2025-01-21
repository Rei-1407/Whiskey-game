document.addEventListener("keydown", function (event) {
    // Kiểm tra nếu phím Esc được nhấn
    if (event.key === "Escape" || event.keyCode === 27) {
        const pausePopUp = document.querySelector('#main .pause');
        pausePopUp.style.display = 'flex';
    }
});

const noBtn = document.querySelector('#main .pause .no-btn');
noBtn.onclick = function() {
    const pausePopUp = document.querySelector('#main .pause');
    pausePopUp.style.display = 'none';
}