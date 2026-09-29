// Point d'entrée du front : relie le formulaire, l'API et l'affichage.

import { applyTheme } from "./theme.js";
import { fetchWeather } from "./weather-api.js";
import { clearStatus, showError, showLoading, showWeather } from "./weather-view.js";
import { loadLastCity, saveLastCity } from "./last-city.js";

const form = document.getElementById("search");
const input = document.getElementById("city");
const submitButton = document.getElementById("go");

async function search(rawCity) {
  const city = rawCity.trim();
  if (!city) return;

  input.value = city;
  submitButton.disabled = true;
  showLoading();

  try {
    const weather = await fetchWeather(city);
    clearStatus();
    applyTheme(weather.vibe.theme);
    showWeather(weather);
    saveLastCity(weather.city);
  } catch (error) {
    showError(error.message);
  } finally {
    submitButton.disabled = false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  search(input.value);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => search(chip.dataset.city));
});

applyTheme("default");
const lastCity = loadLastCity();
if (lastCity) search(lastCity);
