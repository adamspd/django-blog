// run a function that compares the total height to the current position on the page
function updateProgressBar() {
    const {scrollTop, scrollHeight} = document.documentElement;
    const progress = `${(scrollTop / (scrollHeight - window.innerHeight)) * 100}`;
    const scrollPercent = `${(scrollTop / (scrollHeight - window.innerHeight)) * 100}%`;

    // update the progress var to that total height
    document.querySelector('#progress-bar').style.setProperty('--progress', scrollPercent);

    if (progress > 20) {
        document.querySelector('#content-fixed').classList.add("apd-fixed");
    } else if (progress < 20) {
        if (document.querySelector('#content-fixed').classList.contains("apd-fixed")) {
            document.querySelector('#content-fixed').classList.remove("apd-fixed");
        }
    }
}

// event listening to the scroll
document.addEventListener("scroll", updateProgressBar);
