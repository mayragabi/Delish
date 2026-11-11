'use strict';
/* PERSONALIZACIÓN: coloca aquí los nombres reales y fotos del equipo.
   Las fotos son rutas relativas a index.html, por ejemplo: assets/prototipo.jpg.
   No necesitas librerías ni instalar nada para abrir esta página. */
const PROJECT = {
  team: [
    { name: 'Mayra Acosta' },
    { name: 'Samira Quintana' },
    { name: 'Juan Bogado' }
  ],
  photos: [
    { src: '', alt: 'Vista completa del prototipo del basurero inteligente' },
    { src: '', alt: 'Arduino, sensor y conexiones del circuito' },
    { src: '', alt: 'Prueba de detección y apertura de la tapa' }
  ]
};

// Tarjetas del equipo. textContent evita interpretar nombres como código HTML.
const teamGrid = document.querySelector('#team-grid');
PROJECT.team.forEach(member => {
  const card = document.createElement('article');
  card.className = 'team-card reveal';
  const name = document.createElement('h3');
  name.textContent = member.name;
  card.append(name);
  teamGrid.append(card);
});
document.querySelector('#footer-team').textContent = PROJECT.team.map(member => member.name).join(' · ');

// La galería conserva su espacio reservado hasta añadir fotos reales.
PROJECT.photos.forEach((photo, index) => {
  if (!photo.src) return;
  const frame = document.querySelector('[data-gallery="' + index + '"] .gallery-image');
  if (!frame) return;
  const image = new Image();
  image.alt = photo.alt;
  image.loading = 'lazy';
  image.decoding = 'async';
  image.addEventListener('load', () => frame.replaceChildren(image));
  image.src = photo.src;
});

// Navegación para pantallas pequeñas.
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Abrir menú'); navigation.classList.remove('open'); }
menuButton.addEventListener('click', () => { const opened = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(opened)); menuButton.setAttribute('aria-label', opened ? 'Cerrar menú' : 'Abrir menú'); navigation.classList.toggle('open', opened); });
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
document.addEventListener('click', event => { if (!event.target.closest('.header')) closeMenu(); });
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('motion');
  const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } }), { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
}

// Demostración visual. Los tiempos son ilustrativos y no controlan hardware.
const demo = document.querySelector('.demo');
const demoButton = document.querySelector('#demo-button');
const statusText = document.querySelector('#demo-status');
const presence = document.querySelector('#readout-presence');
const lid = document.querySelector('#readout-lid');
const progress = document.querySelector('#demo-progress');
const phase = document.querySelector('#demo-phase');
const steps = [...document.querySelectorAll('.process-step')];
const nodes = [...document.querySelectorAll('.demo-node')];
let demoTimers = [];
let running = false;

function setStep(index) {
  steps.forEach((step, stepIndex) => step.classList.toggle('active', index === stepIndex));
}
function resetDemo() {
  demoTimers.forEach(clearTimeout);
  demoTimers = [];
  running = false;
  demo.classList.remove('running');
  nodes.forEach(node => node.classList.remove('active'));
  setStep(-1);
  presence.textContent = 'Sin detectar';
  lid.textContent = 'Cerrada';
  statusText.textContent = 'Listo para una nueva detección';
  phase.textContent = 'EN ESPERA';
  progress.style.width = '0%';
  demoButton.disabled = false;
  demoButton.querySelector('span').textContent = 'Simular de nuevo';
}
demoButton.addEventListener('click', () => {
  if (running) return;
  running = true;
  demoButton.disabled = true;
  demoButton.querySelector('span').textContent = 'Secuencia en marcha…';
  demo.classList.add('running');
  statusText.textContent = 'Una mano se acerca al sensor';
  phase.textContent = 'ACERCAMIENTO';
  progress.style.width = '20%';
  setStep(0);
  const schedule = (delay, action) => demoTimers.push(setTimeout(action, delay));
  schedule(850, () => { presence.textContent = 'Detectada'; statusText.textContent = 'El sensor detecta la presencia'; nodes[0].classList.add('active'); phase.textContent = 'DETECCIÓN'; progress.style.width = '40%'; setStep(1); });
  schedule(1700, () => { statusText.textContent = 'Arduino procesa la información'; nodes[1].classList.add('active'); phase.textContent = 'PROCESAMIENTO'; progress.style.width = '60%'; setStep(2); });
  schedule(2550, () => { statusText.textContent = 'El servomotor abre la tapa'; lid.textContent = 'Abierta'; nodes[2].classList.add('active'); phase.textContent = 'APERTURA'; progress.style.width = '80%'; setStep(3); });
  schedule(4900, () => { presence.textContent = 'Sin detectar'; lid.textContent = 'Cerrada'; statusText.textContent = 'La tapa se cierra automáticamente'; phase.textContent = 'CIERRE'; progress.style.width = '100%'; setStep(4); });
  schedule(6300, resetDemo);
});
// Si la pestaña queda oculta, volver a un estado listo y coherente.
document.addEventListener('visibilitychange', () => { if (document.hidden && running) resetDemo(); });
