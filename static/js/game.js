// ============================
//  Gyro-Clicker – Hovedvariabler
// ============================
let score = 0;            // Antall «gyros» du har spist
let money = 0;            // Penger brukt til oppgraderinger
let clickPower = 1;       // Hvor mye skade hvert klikk gjør
let autoClickPower = 0;   // Skade per sekund fra auto-klikkere
let cookieHealth = 100;   // Nåværende helse på gyro-ikonet (0 – 100)

// -------------------------------------------------
//  Oppdaterer helse på gyroen hver gang du klikker
// -------------------------------------------------
function updateCookieHealth() {
    cookieHealth -= clickPower;                // Reduser helse med klikk-styrken
    if (cookieHealth <= 0) {                   // Når helsen er tom …
        cookieHealth = 100;                    // … resettes gyroen
        money += 50;                           // Gi spilleren 50 penger
        score++;                               // Øk poengtelleren
        document.getElementById('money').innerText = 'Money: ' + money;
        updateCookieImage();                   // Vis ny gyro-grafikk
    }
    document.getElementById('cookieHealth').innerText = 'Health: ' + cookieHealth + '%';
}

// -------------------------------------------------
//  Bytter bilde basert på hvor «opp-spist» gyroen er
// -------------------------------------------------
function updateCookieImage() {
    let gyroImage = document.getElementById('gyro');
    if (cookieHealth > 75) {
        gyroImage.src = 'static/images/gyrofirstbite.svg';
    } else if (cookieHealth > 50) {
        gyroImage.src = 'static/images/halfgyro.svg';
    } else if (cookieHealth > 25) {
        gyroImage.src = 'static/images/lowhpgyro.svg';
    } else {
        gyroImage.src = 'static/images/criticalhpgyro.svg';
    }
}

// -------------------------------------------------
//  Lager en liten animert «partikkel» der du klikker
// -------------------------------------------------
function createParticleEffect(x, y) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    document.body.appendChild(particle);

    // Fjern partikkelen etter 1 sekund
    setTimeout(() => {
        particle.remove();
    }, 1000);
}

// -------------------------------------------------
//  Spiller en lyd når du klikker på gyroen
// -------------------------------------------------
function playMinecraftSound() {
    const sound = new Audio('static/minecraft_eat.mp3');
    sound.play();
}

// -------------------------------------------------
//  Klikk-hendelse på gyro-bildet
// -------------------------------------------------
document.getElementById('gyro').addEventListener('click', function (event) {
    updateCookieHealth();                                   // Skade gyroen
    document.getElementById('score').innerText = 'Score: ' + score;
    updateCookieImage();                                    // Oppdater bilde
    createParticleEffect(event.clientX, event.clientY);     // Partikkel-effekt
    playMinecraftSound();                                   // Spill lyd
});

// -------------------------------------------------
//  Auto-klikker løkke – kjører hvert 1000 ms (1 sekund)
// -------------------------------------------------
setInterval(function () {
    if (autoClickPower > 0) {
        cookieHealth -= autoClickPower;                     // Skade fra auto
        if (cookieHealth <= 0) {                            // Reset når død
            cookieHealth = 100;
            money += 10;                                    // Mindre penger enn manuell
            score++;
            document.getElementById('money').innerText = 'Money: ' + money;
            updateCookieImage();
        }
        document.getElementById('cookieHealth').innerText = 'Health: ' + cookieHealth + '%';
    }
}, 1000);

// -------------------------------------------------
//  Oppgradering 1 – Øker klikk-styrke
// -------------------------------------------------
document.getElementById('upgrade1').addEventListener('click', function () {
    if (money >= 50) {
        money -= 50;
        clickPower += 1;
        document.getElementById('money').innerText = 'Money: ' + money;
        alert('Oppgradering kjøpt: Sterkere klikk!');
    } else {
        alert('Ikke nok penger til oppgradering.');
    }
});

// -------------------------------------------------
//  Oppgradering 2 – Legger til auto-klikker
// -------------------------------------------------
document.getElementById('upgrade2').addEventListener('click', function () {
    if (money >= 100) {
        money -= 100;
        autoClickPower += 1;
        document.getElementById('money').innerText = 'Money: ' + money;
        alert('Oppgradering kjøpt: Auto-klikker aktiv!');
    } else {
        alert('Ikke nok penger til oppgradering.');
    }
});

// -------------------------------------------------
//  Sender poeng til serveren på en sikker måte (fetch)
// -------------------------------------------------
document.getElementById('submitScore').addEventListener('click', function () {
    fetch('/submit_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score: score })
    })
    .then(response => {
        if (response.ok) {
            alert("Poeng sendt inn!");
            window.location.href = "/leaderboard";          // Gå til ledertavlen
        } else {
            response.json().then(data => {
                alert("Kunne ikke sende poeng: " + (data.error || "Ukjent feil"));
            });
        }
    })
    .catch(err => {
        alert("Feil ved innsending av poeng.");
        console.error(err);
    });
});
