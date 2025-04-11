let score = 0;
let money = 0;
let clickPower = 1;
let autoClickPower = 0;
let cookieHealth = 100;

function updateCookieHealth() {
    cookieHealth -= clickPower;
    if (cookieHealth <= 0) {
        cookieHealth = 100; // Reset cookie health
        money += 50; // Increase money
        score++; // Increase score
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

// Function to create particle effects
function createParticleEffect(x, y) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    document.body.appendChild(particle);

    // Remove particle after animation
    setTimeout(() => {
        particle.remove();
    }, 1000);
}

// Function to play Minecraft sound
function playMinecraftSound() {
    const sound = new Audio('static/minecraft_eat.mp3');
    sound.play();
}

// Add click event listener to the gyro
document.getElementById('gyro').addEventListener('click', function(event) {
    updateCookieHealth();
    document.getElementById('score').innerText = 'Score: ' + score;
    updateCookieImage();

    // Trigger particle effect at click position
    createParticleEffect(event.clientX, event.clientY);

    // Play Minecraft sound
    playMinecraftSound();
});

setInterval(function() {
    if (autoClickPower > 0) {
        cookieHealth -= autoClickPower;
        if (cookieHealth <= 0) {
            cookieHealth = 100; // Reset cookie health
            money += 10; // Increase money
            score++; // Increase score
            document.getElementById('money').innerText = 'Money: ' + money;
            updateCookieImage();
        }
        document.getElementById('cookieHealth').innerText = 'Health: ' + cookieHealth + '%';
    }
}, 1000);

// Implementing upgrades
document.getElementById('upgrade1').addEventListener('click', function() {
    if (money >= 50) {
        money -= 50;
        clickPower += 1;
        document.getElementById('money').innerText = 'Money: ' + money;
        alert('Upgrade purchased: Increased click power');
    } else {
        alert('Not enough money to purchase upgrade.');
    }
});

document.getElementById('upgrade2').addEventListener('click', function() {
    if (money >= 100) {
        money -= 100;
        autoClickPower += 1;
        document.getElementById('money').innerText = 'Money: ' + money;
        alert('Upgrade purchased: Auto-clicker');
    } else {
        alert('Not enough money to purchase upgrade.');
    }
});