// Mémorise la dernière ville cherchée dans le navigateur (le serveur reste sans état).

const STORAGE_KEY = "weather-vibes:last-city";

export function loadLastCity() {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch (_) {
    return null; // stockage bloqué (navigation privée…)
  }
}

export function saveLastCity(city) {
  try {
    localStorage.setItem(STORAGE_KEY, city);
  } catch (_) {
    // pas grave : la ville ne sera simplement pas retenue
  }
}
