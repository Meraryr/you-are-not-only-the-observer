(() => {
  const world = document.querySelector(".world");
  const scene = world.closest(".scene");
  const control = document.querySelector("#motion");
  const lastOceanLine = document.querySelector(".light-line");
  const motionSetting = matchMedia("(prefers-reduced-motion: reduce)");
  const clamp = (value) => Math.min(1, Math.max(0, value));
  const plates = [...world.querySelectorAll(".world-layer")].map((layer) => {
    const section = document.getElementById(layer.dataset.world);
    const cue = { birdsong: 13, umwelt: 40 }[layer.dataset.world];
    return { layer, section, cue: cue ? section.querySelector(`[data-source="${cue}"]`) : null, image: null, ready: false };
  });
  let pending = false;

  function requestPlate(plate) {
    if (plate.image) return;
    const template = plate.layer.querySelector("template");
    const picture = template.content.firstElementChild.cloneNode(true);
    plate.image = picture.querySelector("img");
    plate.image.addEventListener("load", () => {
      plate.ready = true;
      if (plate.cue) {
        plate.layer.style.setProperty("--world-plate", 'url("' + plate.image.currentSrc + '")');
      }
      schedule();
    });
    template.replaceWith(picture);
  }

  function render() {
    pending = false;
    const height = scene.clientHeight;
    if (!height) return;
    const narrow = window.innerWidth <= 820;
    const reduced = motionSetting.matches || control.getAttribute("aria-pressed") === "true";
    const phase = (top, start, span) => {
      const value = clamp((start - top / height) / span);
      return reduced ? Number(value >= .5) : value;
    };
    plates.forEach((plate, index) => {
      const top = plate.section.getBoundingClientRect().top;
      if (top < height * 2.25) requestPlate(plate);
      const opacity = plate.ready ? phase(top, index ? .75 : .24, index ? .64 : .28) : 0;
      plate.layer.style.opacity = opacity.toFixed(4);
      if (plate.cue) {
        plate.layer.style.setProperty("--attention", phase(plate.cue.getBoundingClientRect().top, narrow ? .92 : .83, narrow ? .32 : .46).toFixed(4));
      }
    });
    const returning = phase(lastOceanLine.getBoundingClientRect().bottom, .14, .40);
    world.style.opacity = (1 - returning).toFixed(4);
    scene.style.setProperty("--return-focus", returning.toFixed(4));
  }

  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(render);
  }

  document.documentElement.classList.add("journey-active");
  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", schedule);
  window.addEventListener("pageshow", schedule);
  control.addEventListener("click", schedule);
  motionSetting.addEventListener("change", schedule);
  document.fonts.ready.then(schedule);
  schedule();
})();
