document.addEventListener("DOMContentLoaded", () => {

    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {

        const target = parseInt(counter.innerText);

        let count = 0;

        const speed = Math.max(1, target / 60);

        function updateCounter() {

            if (count < target) {

                count += speed;

                counter.innerText = Math.ceil(count);

                requestAnimationFrame(updateCounter);

            }

            else {

                counter.innerText = target;

            }

        }

        updateCounter();

    });

});