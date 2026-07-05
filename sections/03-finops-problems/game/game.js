import {
  startIconIdle,
  stopIconIdle,
  stopAllIconIdles,
  celebrateIcon,
  enterBlocks,
  snapBlock,
  trimBlock,
  shakeBlock,
  revealLabel,
  revealSvgLabel,
  drawHubPath,
  pulseDropZone,
  popSavings,
  showBanner,
  completeDot,
  showCompletionCard,
  drawFootprintTrail,
  pulseHitZones,
  resetIcon,
  resetHubPaths,
} from "./motion-effects.js";

const PHASES = ["inform", "optimize", "operate"];
const SVG_FILE = "FinOps 3 Phases - visual selection.svg";
const VB = { w: 1044, h: 546 };

const SVG_LABEL_IDS = [
  "g-root-tx_inform_909r2g1nh7rpf-fill",
  "g-root-tx_gainvisi_4mqtk1nh7si4-fill",
  "g-root-tx_optimize_1upxao81nh7t39-fill",
  "g-root-tx_reduceun_1upxao81nh7t3a-fill",
  "g-root-tx_operate_1luwrig1nh7qq7-fill",
  "g-root-tx_embedfin_1hf39e01nh7rig-fill",
];

const ICON_GROUPS = {
  inform: "g-root-cp_2_g-2_1hd7u4o1nh7shv-fill",
  optimize: "g-root-cp_3_g-3_18hktvs1nh7tak-fill",
  operate: "g-root-cp_4_g-4_93zt541okz5s1-fill",
};

const DROPS = {
  inform: { x: 380, y: 175, r: 70 },
  optimize: { x: 640, y: 225, r: 65 },
};

const SLOT_POSITIONS = {
  1: { x: 280, y: 400 },
  2: { x: 360, y: 370 },
  3: { x: 440, y: 360 },
  4: { x: 520, y: 375 },
};

const INFORM_BLOCKS = [
  { id: "untagged", q: "???", reveal: "42% untagged", sub: "no cost-center" },
  { id: "owner", q: "???", reveal: "6 unknown", sub: "no owner" },
  { id: "orphan", q: "???", reveal: "$2.1k/mo", sub: "orphan PVC" },
];

const OPTIMIZE_BLOCKS = [
  { id: "idle", label: "Idle replicas", savings: 2400 },
  { id: "storage", label: "Orphan PVC", savings: 1800 },
  { id: "config", label: "Dup configs", savings: 600 },
];

const OPERATE_BLOCKS = [
  { id: "s1", order: 1, label: "1 · Policy in Git" },
  { id: "s2", order: 2, label: "2 · Cost reviews" },
  { id: "s3", order: 3, label: "3 · Auto agent" },
  { id: "s4", order: 4, label: "4 · Sprint ownership" },
];

const gameState = {
  inform: false,
  optimize: false,
  operate: false,
  activePhase: null,
  informPlaced: new Set(),
  optimizePlaced: new Set(),
  optimizeSaved: 0,
  operatePlaced: 0,
  operateNext: 1,
  selectedBlock: null,
};

let svgDoc = null;
let dragState = null;

const mapStage = document.getElementById("map-stage");
const svgRoot = document.getElementById("svg-root");
const svgObject = document.getElementById("svg-object");
const blocksLayer = document.getElementById("blocks-layer");
const instruction = document.getElementById("instruction");
const phaseBanner = document.getElementById("phase-banner");
const phaseBannerText = document.getElementById("phase-banner-text");
const zoneHub = document.getElementById("zone-hub");
const panelComplete = document.getElementById("panel-complete");
const loadError = document.getElementById("load-error");

const zones = {
  inform: document.getElementById("zone-inform"),
  optimize: document.getElementById("zone-optimize"),
  operate: document.getElementById("zone-operate"),
};

function getIconEl(phase) {
  return svgDoc?.getElementById(ICON_GROUPS[phase]) ?? null;
}

function toPct(x, y) {
  return { left: (x / VB.w) * 100, top: (y / VB.h) * 100 };
}

function waitForObject() {
  return new Promise((resolve) => {
    if (svgObject.contentDocument?.documentElement) {
      resolve(svgObject.contentDocument);
      return;
    }
    svgObject.addEventListener("load", () => resolve(svgObject.contentDocument), { once: true });
  });
}

async function loadSvg() {
  try {
    const res = await fetch(SVG_FILE);
    if (!res.ok) throw new Error("fetch failed");
    const text = await res.text();
    svgRoot.innerHTML = text;
    svgDoc = svgRoot.querySelector("svg");
    if (svgDoc) {
      svgDoc.setAttribute("width", "100%");
      svgDoc.setAttribute("height", "100%");
    }
  } catch {
    svgDoc = await waitForObject();
  }

  if (!svgDoc?.getElementById) {
    loadError?.classList.remove("hidden");
    return;
  }

  hideSvgLabels();
  startAllIconIdles();
}

function hideSvgLabels() {
  SVG_LABEL_IDS.forEach((id) => {
    const el = svgDoc.getElementById(id);
    if (el) el.setAttribute("opacity", "0");
  });
}

function startAllIconIdles() {
  PHASES.forEach((phase) => {
    if (!gameState[phase]) startIconIdle(phase, getIconEl(phase));
  });
}

function revealSvgLabels(phase) {
  const prefixes =
    phase === "inform"
      ? ["g-root-tx_inform", "g-root-tx_gainvisi"]
      : phase === "optimize"
        ? ["g-root-tx_optimize", "g-root-tx_reduceun"]
        : ["g-root-tx_operate", "g-root-tx_embedfin"];

  prefixes.forEach((prefix) => {
    SVG_LABEL_IDS.filter((id) => id.startsWith(prefix)).forEach((id) => {
      revealSvgLabel(svgDoc.getElementById(id));
    });
  });

  revealLabel(document.querySelector(`.phase-label[data-phase="${phase}"]`));
}

function clientToGame(clientX, clientY) {
  const r = mapStage.getBoundingClientRect();
  return {
    x: ((clientX - r.left) / r.width) * VB.w,
    y: ((clientY - r.top) / r.height) * VB.h,
  };
}

function dist(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function setBlockPos(block, x, y) {
  const p = toPct(x, y);
  block.style.left = `${p.left}%`;
  block.style.top = `${p.top}%`;
  block._x = x;
  block._y = y;
}

function createBlock(config) {
  const el = document.createElement("div");
  el.className = `game-block block-${config.phase}`;
  el.dataset.id = config.id;
  el.dataset.phase = config.phase;
  if (config.order) el.dataset.order = config.order;
  if (config.savings) el.dataset.savings = config.savings;

  const main = document.createElement("span");
  main.className = "block-main";
  main.textContent = config.q || config.label || "?";
  el.appendChild(main);

  if (config.sub) {
    const sub = document.createElement("span");
    sub.className = "block-sub";
    sub.textContent = config.sub;
    el.appendChild(sub);
  }

  if (config.reveal) {
    const rev = document.createElement("span");
    rev.className = "block-reveal-text";
    rev.textContent = config.reveal;
    el.appendChild(rev);
  }

  setBlockPos(el, config.x, config.y);
  el._home = { x: config.x, y: config.y };

  el.addEventListener("pointerdown", onBlockPointerDown);
  el.addEventListener("click", (e) => {
    e.stopPropagation();
    selectBlock(el);
  });

  return el;
}

function selectBlock(block) {
  if (block.classList.contains("locked") || !gameState.activePhase) return;
  if (gameState.selectedBlock === block) {
    tryPlaceSelected(block);
    return;
  }
  gameState.selectedBlock?.classList.remove("selected");
  gameState.selectedBlock = block;
  block.classList.add("selected");
  phaseBannerText.textContent = "Block selected — drag it or tap the target zone.";
}

function clearSelection() {
  gameState.selectedBlock?.classList.remove("selected");
  gameState.selectedBlock = null;
}

function tryPlaceSelected(block) {
  const phase = block.dataset.phase;
  if (phase === "inform") placeInformBlock(block);
  else if (phase === "optimize") placeOptimizeBlock(block);
  else if (phase === "operate") placeOperateBlock(block, gameState.operateNext);
}

function onBlockPointerDown(e) {
  const block = e.currentTarget;
  if (block.classList.contains("locked") || !gameState.activePhase) return;
  e.preventDefault();
  e.stopPropagation();

  selectBlock(block);
  block.classList.add("dragging");
  block.setPointerCapture(e.pointerId);

  const pt = clientToGame(e.clientX, e.clientY);
  dragState = {
    block,
    offsetX: block._x - pt.x,
    offsetY: block._y - pt.y,
    pointerId: e.pointerId,
    moved: false,
  };

  block.addEventListener("pointermove", onBlockPointerMove);
  block.addEventListener("pointerup", onBlockPointerUp);
  block.addEventListener("pointercancel", onBlockPointerUp);
}

function onBlockPointerMove(e) {
  if (!dragState || e.pointerId !== dragState.pointerId) return;
  dragState.moved = true;
  const pt = clientToGame(e.clientX, e.clientY);
  setBlockPos(dragState.block, pt.x + dragState.offsetX, pt.y + dragState.offsetY);
  highlightTargets(dragState.block);
}

function onBlockPointerUp(e) {
  if (!dragState || e.pointerId !== dragState.pointerId) return;
  const block = dragState.block;
  block.classList.remove("dragging");
  block.removeEventListener("pointermove", onBlockPointerMove);
  block.removeEventListener("pointerup", onBlockPointerUp);
  block.removeEventListener("pointercancel", onBlockPointerUp);

  clearDropHighlights();
  if (dragState.moved) handleBlockDrop(block);
  dragState = null;
}

function highlightTargets(block) {
  clearDropHighlights();
  const pos = { x: block._x, y: block._y };
  const phase = block.dataset.phase;

  if (phase === "inform" && dist(pos, DROPS.inform) < DROPS.inform.r) {
    pulseDropZone(document.getElementById("drop-inform"), true);
  } else if (phase === "optimize" && dist(pos, DROPS.optimize) < DROPS.optimize.r) {
    pulseDropZone(document.getElementById("drop-optimize"), true);
  } else if (phase === "operate") {
    const slot = findNearestSlot(pos);
    if (slot) document.querySelector(`.slot[data-slot="${slot}"]`)?.classList.add("active");
  }
}

function clearDropHighlights() {
  pulseDropZone(document.getElementById("drop-inform"), false);
  pulseDropZone(document.getElementById("drop-optimize"), false);
  document.querySelectorAll(".slot").forEach((s) => s.classList.remove("active"));
}

function findNearestSlot(pos) {
  let nearest = null;
  let minD = 55;
  Object.entries(SLOT_POSITIONS).forEach(([slot, sp]) => {
    const d = dist(pos, sp);
    if (d < minD) {
      minD = d;
      nearest = Number(slot);
    }
  });
  return nearest;
}

function handleBlockDrop(block) {
  const phase = block.dataset.phase;
  const pos = { x: block._x, y: block._y };

  if (phase === "inform" && dist(pos, DROPS.inform) < DROPS.inform.r) {
    placeInformBlock(block);
  } else if (phase === "optimize" && dist(pos, DROPS.optimize) < DROPS.optimize.r) {
    placeOptimizeBlock(block);
  } else if (phase === "operate") {
    const slot = findNearestSlot(pos);
    if (slot) placeOperateBlock(block, slot);
    else returnBlock(block);
  } else {
    returnBlock(block);
  }
}

async function placeInformBlock(block) {
  if (block.classList.contains("locked") || gameState.informPlaced.has(block.dataset.id)) return;
  const idx = gameState.informPlaced.size;
  await snapBlock(block, 352 + idx * 30, 175, toPct);
  block.classList.add("revealed", "locked");
  clearSelection();
  gameState.informPlaced.add(block.dataset.id);

  if (gameState.informPlaced.size >= 3) {
    setTimeout(() => completePhase("inform"), 400);
  } else {
    updateBanner("inform");
  }
}

async function placeOptimizeBlock(block) {
  if (block.classList.contains("locked") || gameState.optimizePlaced.has(block.dataset.id)) return;
  const savings = Number(block.dataset.savings) || 0;
  block.classList.add("locked");
  clearSelection();
  await trimBlock(block);
  block.remove();
  gameState.optimizePlaced.add(block.dataset.id);
  gameState.optimizeSaved += savings;
  updateSavingsCounter();

  if (gameState.optimizePlaced.size >= 3) {
    setTimeout(() => completePhase("optimize"), 400);
  } else {
    updateBanner("optimize");
  }
}

async function placeOperateBlock(block, slot) {
  if (block.classList.contains("locked")) return;
  if (slot !== gameState.operateNext) {
    await shakeBlock(block);
    phaseBannerText.textContent = `Place step ${gameState.operateNext} next — follow the footprint in order.`;
    return;
  }
  const sp = SLOT_POSITIONS[slot];
  await snapBlock(block, sp.x, sp.y, toPct);
  block.classList.add("locked");
  clearSelection();
  document.querySelector(`.slot[data-slot="${slot}"]`)?.classList.add("filled");
  gameState.operatePlaced++;
  gameState.operateNext++;
  updateFootprintTrail();

  if (gameState.operatePlaced >= 4) {
    setTimeout(() => completePhase("operate"), 400);
  } else {
    updateBanner("operate");
  }
}

function returnBlock(block) {
  if (block._home) snapBlock(block, block._home.x, block._home.y, toPct);
}

function updateSavingsCounter() {
  const g = document.getElementById("savings-float");
  const text = g?.querySelector(".savings-text");
  if (!text) return;
  g.setAttribute("opacity", "1");
  text.textContent = `Saved: $${gameState.optimizeSaved.toLocaleString()}/mo`;
  popSavings(text);
}

function updateFootprintTrail() {
  const trail = document.getElementById("footprint-trail");
  if (!trail || gameState.operatePlaced < 2) return;
  const pts = [];
  for (let i = 1; i <= gameState.operatePlaced; i++) pts.push(SLOT_POSITIONS[i]);
  const d = pts.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");
  drawFootprintTrail(trail, d);
}

function startPhase(phase) {
  if (gameState[phase] || gameState.activePhase) return;

  gameState.activePhase = phase;
  mapStage.classList.add("phase-active");
  zones[phase].classList.add("active-phase");

  stopIconIdle(phase);

  const dropZones = document.getElementById("drop-zones");
  if (dropZones) dropZones.setAttribute("opacity", "1");
  document.getElementById(`drop-${phase}`)?.classList.add("active", phase);

  if (phase === "operate") {
    document.getElementById("footprint-slots")?.setAttribute("opacity", "1");
  }
  if (phase === "optimize") {
    document.getElementById("savings-float")?.setAttribute("opacity", "1");
  }

  updateBanner(phase);
  spawnBlocks(phase);

  const target =
    phase === "inform" ? "binoculars" : phase === "optimize" ? "trim zone" : "numbered slots";
  instruction.innerHTML = `Drag blocks to the <strong>${target}</strong> (or tap block, then tap target).`;
}

function endPhaseUI(clearBlocks) {
  gameState.activePhase = null;
  clearSelection();
  mapStage.classList.remove("phase-active");
  PHASES.forEach((p) => zones[p].classList.remove("active-phase"));

  document.getElementById("drop-zones")?.setAttribute("opacity", "0");
  document.getElementById("footprint-slots")?.setAttribute("opacity", "0");
  document.querySelectorAll(".drop-zone").forEach((dz) => dz.classList.remove("active", "inform", "optimize", "operate"));
  phaseBanner.classList.add("hidden");

  if (clearBlocks) blocksLayer.innerHTML = "";
}

function spawnBlocks(phase) {
  blocksLayer.innerHTML = "";
  const blocks = [];

  const add = (config, home) => {
    const block = createBlock({ ...config, x: home.x, y: home.y });
    block._home = { ...home };
    blocksLayer.appendChild(block);
    blocks.push(block);
  };

  if (phase === "inform") {
    const starts = [
      { x: 120, y: 200 },
      { x: 165, y: 265 },
      { x: 95, y: 325 },
    ];
    INFORM_BLOCKS.forEach((b, i) => add({ ...b, phase: "inform" }, starts[i]));
  } else if (phase === "optimize") {
    const starts = [
      { x: 585, y: 205 },
      { x: 615, y: 248 },
      { x: 595, y: 288 },
    ];
    OPTIMIZE_BLOCKS.forEach((b, i) => add({ ...b, phase: "optimize" }, starts[i]));
  } else if (phase === "operate") {
    const shuffled = [...OPERATE_BLOCKS].sort(() => Math.random() - 0.5);
    const starts = [
      { x: 130, y: 425 },
      { x: 195, y: 455 },
      { x: 90, y: 475 },
      { x: 235, y: 415 },
    ];
    shuffled.forEach((b, i) => add({ ...b, phase: "operate" }, starts[i]));
  }

  enterBlocks(blocks);
}

function updateBanner(phase) {
  const msgs = {
    inform: () => `Reveal blind spots: ${gameState.informPlaced.size}/3 → binoculars`,
    optimize: () => `Trim waste: ${gameState.optimizePlaced.size}/3 → trim zone`,
    operate: () => `Footprint step ${gameState.operateNext} of 4 — drag to numbered slot`,
  };
  phaseBannerText.textContent = msgs[phase]?.() || "";
  showBanner(phaseBanner);
}

function completePhase(phase) {
  if (gameState[phase]) return;
  gameState[phase] = true;

  endPhaseUI(true);
  celebrateIcon(phase, getIconEl(phase));
  revealSvgLabels(phase);

  const path = document.getElementById(`path-${phase}`);
  const hubPaths = document.getElementById("hub-paths");
  drawHubPath(path, hubPaths);

  zones[phase].classList.add("completed");
  zones[phase].classList.remove("pulse");

  completeDot(document.querySelector(`.dot[data-phase="${phase}"]`));
  updateInstruction();

  if (PHASES.every((p) => gameState[p])) {
    setTimeout(() => showCompletionCard(panelComplete), 400);
  }
}

function updateInstruction() {
  const remaining = PHASES.filter((p) => !gameState[p]);
  if (remaining.length === 0) {
    instruction.innerHTML = "All phases complete! Click the <strong>cluster</strong> for the summary.";
    zoneHub.disabled = false;
    return;
  }
  const labels = { inform: "binoculars", optimize: "sailboat", operate: "boot" };
  instruction.innerHTML = `Click the <strong>${remaining.map((p) => labels[p]).join("</strong>, <strong>")}</strong> to start.`;
}

function resetGame() {
  Object.assign(gameState, {
    inform: false,
    optimize: false,
    operate: false,
    activePhase: null,
    informPlaced: new Set(),
    optimizePlaced: new Set(),
    optimizeSaved: 0,
    operatePlaced: 0,
    operateNext: 1,
    selectedBlock: null,
  });

  endPhaseUI(true);
  panelComplete.classList.add("hidden");
  panelComplete.style.opacity = "";
  panelComplete.style.transform = "";
  zoneHub.disabled = true;

  document.getElementById("footprint-trail")?.setAttribute("d", "");
  document.getElementById("savings-float")?.setAttribute("opacity", "0");
  document.querySelectorAll(".slot").forEach((s) => s.classList.remove("filled", "active"));

  resetHubPaths(document.getElementById("hub-paths"));

  PHASES.forEach((phase) => {
    zones[phase].classList.remove("completed");
    zones[phase].classList.add("pulse");
    resetIcon(getIconEl(phase));
  });

  stopAllIconIdles();
  document.querySelectorAll(".phase-label").forEach((el) => {
    el.classList.remove("revealed");
    el.style.opacity = "";
    el.style.transform = "";
  });
  hideSvgLabels();
  startAllIconIdles();
  pulseHitZones([zones.inform, zones.optimize, zones.operate]);
  updateProgressDots();
  updateInstruction();
}

function updateProgressDots() {
  PHASES.forEach((phase) => {
    document.querySelector(`.dot[data-phase="${phase}"]`)?.classList.toggle("done", gameState[phase]);
  });
}

function initEvents() {
  zones.inform.addEventListener("click", () => {
    if (!gameState.inform && !gameState.activePhase) startPhase("inform");
  });
  zones.optimize.addEventListener("click", () => {
    if (!gameState.optimize && !gameState.activePhase) startPhase("optimize");
  });
  zones.operate.addEventListener("click", () => {
    if (!gameState.operate && !gameState.activePhase) startPhase("operate");
  });

  zoneHub.addEventListener("click", () => {
    if (PHASES.every((p) => gameState[p])) showCompletionCard(panelComplete);
  });

  document.getElementById("phase-banner-close").addEventListener("click", () => {
    const phase = gameState.activePhase;
    if (!phase) return;
    endPhaseUI(true);
    startIconIdle(phase, getIconEl(phase));
    updateInstruction();
  });

  document.getElementById("btn-replay").addEventListener("click", resetGame);

  mapStage.addEventListener("click", (e) => {
    if (!gameState.activePhase || !gameState.selectedBlock) return;
    if (e.target.closest(".game-block")) return;

    const pt = clientToGame(e.clientX, e.clientY);
    const phase = gameState.selectedBlock.dataset.phase;

    if (phase === "inform" && dist(pt, DROPS.inform) < DROPS.inform.r + 20) {
      placeInformBlock(gameState.selectedBlock);
    } else if (phase === "optimize" && dist(pt, DROPS.optimize) < DROPS.optimize.r + 20) {
      placeOptimizeBlock(gameState.selectedBlock);
    } else if (phase === "operate") {
      const slot = findNearestSlot(pt);
      if (slot) placeOperateBlock(gameState.selectedBlock, slot);
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (!panelComplete.classList.contains("hidden")) {
        panelComplete.classList.add("hidden");
      } else if (gameState.activePhase) {
        const exiting = gameState.activePhase;
        endPhaseUI(true);
        startIconIdle(exiting, getIconEl(exiting));
        updateInstruction();
      }
    }
  });
}

async function init() {
  initEvents();
  await loadSvg();
  pulseHitZones([zones.inform, zones.optimize, zones.operate]);
  updateProgressDots();
  updateInstruction();
}

init();
