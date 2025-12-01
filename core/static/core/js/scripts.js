
const countdownElement = document.getElementById('countdown');

const fechaEventoString = countdownElement.dataset.fechaEvento;
const fechaEvento = moment.utc(fechaEventoString);

const days = document.getElementById('days');
const hours = document.getElementById('hours');
const minutes = document.getElementById('minutes');
const seconds = document.getElementById('seconds');

function Counter() {
  const now = moment();
  const duration = moment.duration(fechaEvento.diff(now));

  if (duration.asSeconds() <= 0) {
    document.getElementById('comenzo').textContent = "¡El evento ha comenzado!";
    clearInterval(intervalo);
    return;
  }

  days.textContent = Math.floor(duration.asDays()).toString().padStart(2, '0');
  hours.textContent = duration.hours().toString().padStart(2, '0');
  minutes.textContent = duration.minutes().toString().padStart(2, '0');
  seconds.textContent = duration.seconds().toString().padStart(2, '0');
}

const intervalo = setInterval(Counter, 1000);
Counter();


