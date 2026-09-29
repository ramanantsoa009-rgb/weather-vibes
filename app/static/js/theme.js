// Applique le thème visuel (couleurs, particules) sur la page.

import { renderSky } from "./sky.js";

const THEMES = ["sunny", "cloudy", "rainy", "storm", "snowy", "foggy", "night", "default"];
const DEFAULT_THEME = "default";

export function applyTheme(theme) {
  const safeTheme = THEMES.includes(theme) ? theme : DEFAULT_THEME;
  THEMES.forEach((name) => document.body.classList.remove("theme-" + name));
  document.body.classList.add("theme-" + safeTheme);
  renderSky(document.getElementById("sky"), safeTheme);
}
