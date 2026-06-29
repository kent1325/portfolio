const heroLines = Array.from(document.querySelectorAll(".hero__line"));

function getSharedPrefix(values) {
    if (values.length === 0) {
        return "";
    }

    let prefix = values[0];

    for (const value of values.slice(1)) {
        while (!value.startsWith(prefix) && prefix.length > 0) {
            prefix = prefix.slice(0, -1);
        }
    }

    return prefix;
}

if (
    heroLines.length > 1 &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
) {
    const visibleLine = heroLines[0];
    const lines = heroLines.map((line) => line.textContent.trim());
    const sharedPrefix = getSharedPrefix(lines);

    let lineIndex = 0;
    let characterIndex = 0;
    let isDeleting = false;

    visibleLine.textContent = "";

    function typeLine() {
        const currentLine = lines[lineIndex];
        const isLastLine = lineIndex === lines.length - 1;
        const deleteUntilLength = isLastLine ? 0 : sharedPrefix.length;

        if (isDeleting) {
            characterIndex -= 1;
        } else {
            characterIndex += 1;
        }

        visibleLine.textContent = currentLine.slice(0, characterIndex);

        if (!isDeleting && characterIndex === currentLine.length) {
            isDeleting = true;
            setTimeout(typeLine, 1400);
            return;
        }

        if (isDeleting && characterIndex === deleteUntilLength) {
            isDeleting = false;
            lineIndex = (lineIndex + 1) % lines.length;
        }

        setTimeout(typeLine, isDeleting ? 45 : 85);
    }

    typeLine();
}
