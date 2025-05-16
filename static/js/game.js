let score = 0;
let money = 0;
let clickPower = 1;
let autoClickPower = 0;
let cookieHealth = 100;

function updateCookieHealth() {
    cookieHealth -= clickPower;
    if (cookieHealth <= 0) {
        cookieHealth = 100;
        money += 50;
        score++;
        document.getElementById('money').innerText = 'Money: ' + money;
        updateCookieImage();
    }
    document.getElementById('cookieHealth').innerText = 'Health: ' + cookieHealth + '%';
}

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

function createParticleEffect(x, y) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    document.body.appendChild(particle);

    setTimeout(() => {
        particle.remove();
    }, 1000);
}

function playMinecraftSound() {
    const sound = new Audio('static/minecraft_eat.mp3');
    sound.play();
}

document.getElementById('gyro').addEventListener('click', function (event) {
    updateCookieHealth();
    document.getElementById('score').innerText = 'Score: ' + score;
    updateCookieImage();
    createParticleEffect(event.clientX, event.clientY);
    playMinecraftSound();
});

setInterval(function () {
    if (autoClickPower > 0) {
        cookieHealth -= autoClickPower;
        if (cookieHealth <= 0) {
            cookieHealth = 100;
            money += 10;
            score++;
            document.getElementById('money').innerText = 'Money: ' + money;
            updateCookieImage();
        }
        document.getElementById('cookieHealth').innerText = 'Health: ' + cookieHealth + '%';
    }
}, 1000);

document.getElementById('upgrade1').addEventListener('click', function () {
    if (money >= 50) {
        money -= 50;
        clickPower += 1;
        document.getElementById('money').innerText = 'Money: ' + money;
        alert('Upgrade purchased: Increased click power');
    } else {
        alert('Not enough money to purchase upgrade.');
    }
});

document.getElementById('upgrade2').addEventListener('click', function () {
    if (money >= 100) {
        money -= 100;
        autoClickPower += 1;
        document.getElementById('money').innerText = 'Money: ' + money;
        alert('Upgrade purchased: Auto-clicker');
    } else {
        alert('Not enough money to purchase upgrade.');
    }
});

// ✅ Securely submit score via fetch
document.getElementById('submitScore').addEventListener('click', function () {
    fetch('/submit_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ score: score })
    })
    .then(response => {
        if (response.ok) {
            alert("Score submitted!");
            window.location.href = "/leaderboard";
        } else {
            response.json().then(data => {
                alert("Failed to submit score: " + (data.error || "Unknown error"));
            });
        }
    })
    .catch(err => {
        alert("Error submitting score.");
        console.error(err);
    });
});
