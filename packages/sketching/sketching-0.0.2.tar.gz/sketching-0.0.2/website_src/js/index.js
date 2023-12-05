const USE_CASES = [
    "interactive science",
    "data visualizations",
    "visual art",
    "simulations",
    "UX prototypes",
    "games",
    "lessons"
];

const PLATFORMS = [
    "desktop",
    "laptop",
    "web",
    "browser",
    "mobile",
    "server",
    "Jupyter",
    "notebooks"
];


function transition() {
    const useCase = USE_CASES[Math.floor(Math.random() * USE_CASES.length)];
    const platform = PLATFORMS[Math.floor(Math.random() * PLATFORMS.length)];

    const useCaseElem = document.getElementById("use-case");
    const platformElem = document.getElementById("platform");

    useCaseElem.innerHTML = useCase;
    platformElem.innerHTML = platform;

    const applyAnimation = (elem) => {
        elem.animate(
            [
                { opacity: 0 },
                { opacity: 1 }
            ],
            {
                duration: 1000,
                iterations: 1
            }
        );
    };

    applyAnimation(useCaseElem);
    applyAnimation(platformElem);

    setTimeout(transition, 6000);
}


transition();
