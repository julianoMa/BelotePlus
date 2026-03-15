document.addEventListener("DOMContentLoaded", () => {
    const wrappers = document.querySelectorAll("#scroll");

    const step = 150;
    const interval = 5000;

    wrappers.forEach(wrapper => {
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
});