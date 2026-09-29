// Affichage : carte météo, message de chargement et message d'erreur.

const byId = (id) => document.getElementById(id);

// Une illustration animée par thème : sunny.svg, rainy.svg… (voir static/images/weather/README.md)
const ILLUSTRATION_DIR = "/static/images/weather/";
const ILLUSTRATION_EXTENSION = ".svg";

function setStat(name, value, unit) {
  const box = byId("stat-" + name);
  box.hidden = value === null || value === undefined;
  if (!box.hidden) byId(name).textContent = value + unit;
}

function roundOrNull(value) {
  return value === null || value === undefined ? null : Math.round(value);
}

function showIllustration(theme, description) {
  const illustration = byId("weather-illustration");
  illustration.onload = () => { illustration.hidden = false; };
  illustration.onerror = () => { illustration.hidden = true; }; // fichier absent : on n'affiche rien
  illustration.alt = description;
  illustration.src = ILLUSTRATION_DIR + theme + ILLUSTRATION_EXTENSION;
}

function replayCardAnimation(card) {
  card.hidden = true;
  void card.offsetWidth; // force un reflow pour relancer l'animation CSS
  card.hidden = false;
}

export function showWeather(data) {
  byId("place").textContent = data.city;

  const country = byId("country");
  country.hidden = !data.country;
  country.textContent = data.country || "";

  showIllustration(data.vibe.theme, data.description);

  byId("temp").textContent = Math.round(data.temperature);
  byId("description").textContent = data.description;
  byId("vibe").textContent = data.vibe.message;

  setStat("feels", roundOrNull(data.feels_like), "°");
  setStat("humidity", data.humidity, "%");
  setStat("wind", roundOrNull(data.wind), " km/h");

  replayCardAnimation(byId("card"));
}

export function showLoading() {
  const status = byId("status");
  status.className = "status";
  const loader = document.createElement("span");
  loader.className = "loader";
  loader.textContent = "🌀";
  status.replaceChildren(loader, " Je consulte le ciel…");
}

function shakeSearchForm() {
  const form = byId("search");
  form.classList.remove("shake");
  void form.offsetWidth; // force un reflow pour pouvoir rejouer l'animation
  form.classList.add("shake");
}

export function showError(message) {
  const status = byId("status");
  status.className = "status error";
  status.textContent = message;
  shakeSearchForm();
}

export function clearStatus() {
  const status = byId("status");
  status.className = "status";
  status.textContent = "";
}
