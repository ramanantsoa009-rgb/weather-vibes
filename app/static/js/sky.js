// Particules d'ambiance en fond d'écran (pluie, neige, étoiles…) selon le thème.

const SMALL_SCREEN_WIDTH = 600;

function random(min, max) {
  return Math.random() * (max - min) + min;
}

function spawnParticles(sky, className, count, setup) {
  const fragment = document.createDocumentFragment();
  for (let i = 0; i < count; i++) {
    const particle = document.createElement("span");
    particle.className = "particle " + className;
    setup(particle, i);
    fragment.appendChild(particle);
  }
  sky.appendChild(fragment);
}

function rain(sky, count) {
  spawnParticles(sky, "drop", count, (drop) => {
    drop.style.left = random(0, 110) + "vw";
    drop.style.animationDuration = random(0.5, 0.9) + "s";
    drop.style.animationDelay = random(-1, 0) + "s";
    drop.style.opacity = random(0.4, 1);
  });
}

function snow(sky, count) {
  spawnParticles(sky, "flake", count, (flake) => {
    flake.textContent = Math.random() > 0.5 ? "❄" : "•";
    flake.style.left = random(0, 100) + "vw";
    flake.style.fontSize = random(8, 20) + "px";
    flake.style.animationDuration = random(6, 14) + "s";
    flake.style.animationDelay = random(-14, 0) + "s";
  });
}

function stars(sky, count) {
  spawnParticles(sky, "star", count, (star) => {
    star.style.left = random(0, 100) + "vw";
    star.style.top = random(0, 100) + "vh";
    star.style.animationDuration = random(2, 5) + "s";
    star.style.animationDelay = random(-5, 0) + "s";
  });
}

function sparkles(sky, count) {
  spawnParticles(sky, "sparkle", count, (sparkle) => {
    sparkle.textContent = "✦";
    sparkle.style.left = random(0, 100) + "vw";
    sparkle.style.top = random(0, 100) + "vh";
    sparkle.style.fontSize = random(10, 22) + "px";
    sparkle.style.animationDuration = random(2, 4) + "s";
    sparkle.style.animationDelay = random(-4, 0) + "s";
  });
}

function clouds(sky) {
  spawnParticles(sky, "cloud-puff", 6, (cloud, i) => {
    cloud.style.top = 8 + i * 15 + "vh";
    cloud.style.transform = "scale(" + random(0.6, 1.3) + ")";
    cloud.style.animationDuration = random(35, 60) + "s";
    cloud.style.animationDelay = random(-60, 0) + "s";
  });
}

function fog(sky) {
  spawnParticles(sky, "fog-band", 6, (band, i) => {
    band.style.top = 5 + i * 16 + "vh";
    band.style.animationDuration = random(25, 45) + "s";
    band.style.animationDelay = random(-45, 0) + "s";
  });
}

export function renderSky(sky, theme) {
  sky.replaceChildren();
  const isSmall = window.innerWidth < SMALL_SCREEN_WIDTH;

  switch (theme) {
    case "rainy":
    case "storm":
      return rain(sky, isSmall ? 50 : 100);
    case "snowy":
      return snow(sky, isSmall ? 30 : 60);
    case "night":
      return stars(sky, isSmall ? 40 : 80);
    case "sunny":
    case "default":
      return sparkles(sky, isSmall ? 12 : 22);
    case "cloudy":
      return clouds(sky);
    case "foggy":
      return fog(sky);
  }
}
