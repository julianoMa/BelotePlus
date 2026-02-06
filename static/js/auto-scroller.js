document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.querySelector(".teams-wrapper");

    const step = 100;
    const interval = 1000;
    let direction = 1;

    setInterval(() => {
        const maxScroll = wrapper.scrollHeight - wrapper.clientHeight;

        wrapper.scrollTop += step * direction;

        if (wrapper.scrollTop >= maxScroll) {
            direction = -1;
        }

        if (wrapper.scrollTop <= 0) {
            direction = 1;
        }
    }, interval);
});