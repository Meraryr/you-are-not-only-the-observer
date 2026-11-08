const scene = document.querySelector(".scene");
const opening = document.querySelector(".opening");
const trap = document.querySelector(".trap");
const recognition = document.querySelector(".recognition");
const motionButton = document.querySelector("#motion");
const motionPreference = matchMedia("(prefers-reduced-motion: reduce)");
let manuallyReduced = false;
let scheduled = false;

const clamp = (value) => Math.min(1, Math.max(0, value));

function renderFocus() {
  scheduled = false;
  const height = scene.clientHeight;
  const trapTop = trap.getBoundingClientRect().top / height;
  const openingTop = opening.getBoundingClientRect().top / height;
  const recognitionTop = recognition.getBoundingClientRect().top / height;
  const narrow = window.innerWidth <= 760;
  // On narrow screens the image resolves before the trap line enters.
  const progress = narrow
    ? clamp((1.46 - trapTop) / 0.31)
    : clamp((0.81 - trapTop) / 0.37);
  const reduced = motionPreference.matches || manuallyReduced;
  const focus = reduced ? Number(progress >= 0.5) : progress;
  const openingShade = clamp((0.88 - openingTop) / 0.64);
  const turnShade = narrow
    ? 1 - clamp((1.92 - trapTop) / 0.53)
    : 1 - clamp((1.07 - trapTop) / 0.64);
  const finalShade = clamp((0.8 - recognitionTop) / 0.55);
  const shade = Math.max(openingShade * turnShade, finalShade * 0.72);
  scene.style.setProperty("--focus", focus.toFixed(4));
  scene.style.setProperty("--shade", (reduced ? Number(shade >= 0.5) : shade).toFixed(4));
}

function scheduleFocus() {
  if (!scheduled) {
    scheduled = true;
    requestAnimationFrame(renderFocus);
  }
}

function updateMotion() {
  motionButton.disabled = motionPreference.matches;
  motionButton.setAttribute("aria-pressed", String(motionPreference.matches || manuallyReduced));
  scheduleFocus();
}

motionButton.addEventListener("click", () => {
  manuallyReduced = !manuallyReduced;
  updateMotion();
});
motionPreference.addEventListener("change", updateMotion);
window.addEventListener("scroll", scheduleFocus, { passive: true });
window.addEventListener("resize", scheduleFocus);
window.addEventListener("pageshow", scheduleFocus);
document.fonts.ready.then(scheduleFocus);
motionButton.hidden = false;
updateMotion();
