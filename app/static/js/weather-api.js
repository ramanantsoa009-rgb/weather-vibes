// Appel au backend GET /weather. Renvoie les données ou lève une Error au message lisible.

const GENERIC_ERROR = "Oups, quelque chose s'est mal passé.";
const NETWORK_ERROR = "Impossible de joindre le serveur. Vérifie ta connexion.";

async function readJson(response) {
  try {
    return await response.json();
  } catch (_) {
    return null;
  }
}

function errorMessageFor(response, body) {
  if (body && typeof body.detail === "string") return body.detail;
  if (response.status === 422) return "Nom de ville invalide.";
  return GENERIC_ERROR;
}

export async function fetchWeather(city) {
  let response;
  try {
    response = await fetch("/weather?city=" + encodeURIComponent(city));
  } catch (_) {
    throw new Error(NETWORK_ERROR);
  }

  const body = await readJson(response);
  if (!response.ok) throw new Error(errorMessageFor(response, body));
  return body;
}
