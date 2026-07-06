const themeStorageKey = "portfolio-theme";
const lightThemeColor = "#f8fafc";
const darkThemeColor = "#020617";
const themeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
const themeToggleButtons = Array.from(document.querySelectorAll("[data-theme-toggle]"));
const themeColorMeta = document.querySelector("[data-theme-color]");

function readStoredTheme() {
    try {
        const theme = localStorage.getItem(themeStorageKey);
        return theme === "dark" || theme === "light" ? theme : null;
    } catch {
        return null;
    }
}

let storedThemeOverride = readStoredTheme();

function getStoredTheme() {
    return storedThemeOverride;
}

function storeTheme(theme) {
    storedThemeOverride = theme;

    try {
        localStorage.setItem(themeStorageKey, theme);
    } catch {
        // Ignore storage errors; the visible theme still changes for this page load.
    }
}

function getResolvedTheme() {
    return getStoredTheme() ?? (themeMediaQuery.matches ? "dark" : "light");
}

function applyStoredTheme() {
    const storedTheme = getStoredTheme();

    if (storedTheme) {
        document.documentElement.dataset.theme = storedTheme;
        document.documentElement.style.colorScheme = storedTheme;
        return;
    }

    delete document.documentElement.dataset.theme;
    document.documentElement.style.colorScheme = themeMediaQuery.matches ? "dark" : "light";
}

function updateThemeColor() {
    if (!themeColorMeta) {
        return;
    }

    themeColorMeta.setAttribute(
        "content",
        getResolvedTheme() === "dark" ? darkThemeColor : lightThemeColor
    );
}

function updateThemeToggleButtons() {
    const resolvedTheme = getResolvedTheme();
    const nextTheme = resolvedTheme === "dark" ? "light" : "dark";

    for (const button of themeToggleButtons) {
        const icon = button.querySelector("[data-theme-toggle-icon]");
        const text = button.querySelector("[data-theme-toggle-text]");

        button.hidden = false;
        button.setAttribute("aria-label", `Switch to ${nextTheme} mode`);
        button.setAttribute("aria-pressed", resolvedTheme === "dark" ? "true" : "false");

        if (icon) {
            icon.textContent = nextTheme === "dark" ? "☾" : "☀";
        }

        if (text) {
            text.textContent = nextTheme === "dark" ? "Dark" : "Light";
        }
    }
}

function syncTheme() {
    applyStoredTheme();
    updateThemeColor();
    updateThemeToggleButtons();
}

for (const button of themeToggleButtons) {
    button.addEventListener("click", () => {
        const nextTheme = getResolvedTheme() === "dark" ? "light" : "dark";
        storeTheme(nextTheme);
        syncTheme();
    });
}

if (typeof themeMediaQuery.addEventListener === "function") {
    themeMediaQuery.addEventListener("change", syncTheme);
} else if (typeof themeMediaQuery.addListener === "function") {
    themeMediaQuery.addListener(syncTheme);
}

syncTheme();
