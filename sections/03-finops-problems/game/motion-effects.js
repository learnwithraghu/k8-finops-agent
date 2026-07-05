import { animate } from "https://cdn.jsdelivr.net/npm/motion@12.23.12/+esm";

const idleLoops = new Map();
const CENTER = "translate(-50%, -50%)";
const SPRING_SNAP = { type: "spring", stiffness: 380, damping: 26 };
const SPRING_SOFT = { type: "spring", stiffness: 320, damping: 22 };
const SPRING_POP = { type: "spring", stiffness: 400, damping: 12 };
const SPRING_CELEBRATE = { type: "spring", stiffness: 260, damping: 14 };

/** Idle float on SVG icon groups until phase completes */
export function startIconIdle(phase, el) {
  if (!el) return;
  stopIconIdle(phase);

  const configs = {
    inform: { y: [0, -7, 0], rotate: [-3, 3, -3], duration: 3.2 },
    optimize: { y: [0, -5, 0], rotate: [-4, 4, -4], duration: 2.8 },
    operate: { y: [0, -4, 0], rotate: [0, 0, 0], duration: 3.4 },
  };
  const c = configs[phase] || configs.inform;

  const controls = animate(el, { y: c.y, rotate: c.rotate }, { duration: c.duration, repeat: Infinity, ease: "easeInOut" });
  idleLoops.set(phase, controls);
}

export function stopIconIdle(phase) {
  idleLoops.get(phase)?.stop();
  idleLoops.delete(phase);
}

export function stopAllIconIdles() {
  idleLoops.forEach((c) => c.stop());
  idleLoops.clear();
}

/** Phase-complete celebration on SVG icon */
export function celebrateIcon(phase, el) {
  if (!el) return;
  stopIconIdle(phase);
  return animate(
    el,
    { scale: [1, 1.18, 1], rotate: phase === "optimize" ? [0, -6, 4, 0] : [0, 0, 0] },
    { duration: 0.75, ...SPRING_CELEBRATE },
  );
}

/** Stagger blocks appearing at phase start */
export function enterBlocks(blocks) {
  return Promise.all(
    [...blocks].map((b, i) => {
      b.style.opacity = "0";
      b.style.transform = `${CENTER} scale(0.6)`;
      return animate(b, { opacity: 1, scale: 1 }, { delay: i * 0.1, duration: 0.45, ...SPRING_SOFT }).finished;
    }),
  );
}

/** Spring snap block to game coordinates */
export function snapBlock(block, x, y, toPct) {
  const p = toPct(x, y);
  block.style.left = `${p.left}%`;
  block.style.top = `${p.top}%`;
  block._x = x;
  block._y = y;
  block.style.transform = `${CENTER} scale(1.12)`;
  return animate(block, { scale: 1 }, { duration: 0.45, ...SPRING_SNAP }).finished;
}

/** Optimize: trim block flies off the boat */
export function trimBlock(block) {
  block.style.transform = `${CENTER} rotate(0deg) scale(1)`;
  return animate(block, { opacity: 0, x: 80, y: -50, rotate: 18, scale: 0.4 }, { duration: 0.45, ease: "easeIn" }).finished;
}

/** Wrong operate placement */
export function shakeBlock(block) {
  return animate(block, { x: [0, -8, 8, -5, 5, 0] }, { duration: 0.4 }).finished;
}

/** Reveal phase label overlay */
export function revealLabel(el) {
  if (!el) return;
  el.classList.add("revealed");
  el.style.opacity = "0";
  el.style.transform = "translateY(10px)";
  return animate(el, { opacity: 1, y: 0 }, { duration: 0.5, ease: "easeOut" }).finished;
}

/** Fade in SVG text label inside diagram */
export function revealSvgLabel(el) {
  if (!el) return;
  return animate(el, { opacity: 1 }, { duration: 0.5 }).finished;
}

/** Draw hub connection path */
export function drawHubPath(pathEl, groupEl) {
  if (!pathEl) return;
  if (groupEl) animate(groupEl, { opacity: 1 }, { duration: 0.3 });
  return animate(pathEl, { pathLength: 1 }, { duration: 1.1, ease: "easeInOut" }).finished;
}

/** Pulse drop zone while block is near */
export function pulseDropZone(el, active) {
  if (!el) return;
  if (active) {
    el._pulse?.stop();
    el._pulse = animate(el, { scale: [1, 1.06, 1] }, { duration: 1.2, repeat: Infinity, ease: "easeInOut" });
  } else {
    el._pulse?.stop();
    animate(el, { scale: 1 }, { duration: 0.2 });
  }
}

/** Savings counter pop */
export function popSavings(el) {
  if (!el) return;
  return animate(el, { scale: [1, 1.12, 1] }, { duration: 0.35, ...SPRING_POP }).finished;
}

/** Show phase banner */
export function showBanner(el) {
  if (!el) return;
  el.classList.remove("hidden");
  el.style.transform = "translateX(-50%) translateY(-10px)";
  el.style.opacity = "0";
  return animate(el, { opacity: 1, y: 0 }, { duration: 0.35, ease: "easeOut" }).finished;
}

/** Progress dot completes */
export function completeDot(dot) {
  if (!dot) return;
  return animate(dot, { scale: [1, 1.35, 1.15] }, { duration: 0.4, ...SPRING_CELEBRATE }).finished;
}

/** Completion card entrance */
export function showCompletionCard(el) {
  if (!el) return;
  el.classList.remove("hidden");
  el.style.transform = "translate(-50%, -50%) scale(0.88)";
  el.style.opacity = "0";
  return animate(el, { opacity: 1, scale: 1 }, { duration: 0.45, type: "spring", stiffness: 280, damping: 20 }).finished;
}

/** Reset icon transform after replay */
export function resetIcon(el) {
  if (!el) return;
  return animate(el, { scale: 1, rotate: 0, y: 0, x: 0 }, { duration: 0.2 }).finished;
}

/** Reset hub paths for replay */
export function resetHubPaths(groupEl) {
  if (!groupEl) return;
  groupEl.querySelectorAll(".hub-path").forEach((path) => {
    animate(path, { pathLength: 0 }, { duration: 0 });
  });
  animate(groupEl, { opacity: 0 }, { duration: 0.2 });
}

/** Zone hint pulse on load */
export function pulseHitZones(zones) {
  zones.forEach((z, i) => {
    if (!z || z.classList.contains("completed")) return;
    animate(
      z,
      {
        boxShadow: [
          "0 0 0 0 rgba(88,64,83,0)",
          "inset 0 0 0 3px rgba(88,64,83,0.12)",
          "0 0 0 0 rgba(88,64,83,0)",
        ],
      },
      { duration: 2.4, repeat: Infinity, delay: i * 0.3 },
    );
  });
}

/** Footprint trail draw */
export function drawFootprintTrail(pathEl, d) {
  if (!pathEl) return;
  pathEl.setAttribute("d", d);
  pathEl.style.opacity = "0";
  return animate(pathEl, { pathLength: 1, opacity: 0.7 }, { duration: 0.5, ease: "easeOut" }).finished;
}
