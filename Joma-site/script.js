const phrases = [
    "No",
    "Are you sure?",
    "Really sure?",
    "Think again!",
    "Last chance!",
    "Surely not?",
    "You might regret this!",
    "Give it another thought!",
    "Are you absolutely certain?",
    "This could be a mistake!",
    "Have a heart!",
    "Don't be so cold!",
    "Change of heart?",
    "Wouldn't you reconsider?",
    "Is that your final answer?",
    "You're breaking my heart ;(",
];

let noCount = 0;
const noBtn = document.getElementById('no-btn');
const yesBtn = document.getElementById('yes-btn');
const gif = document.getElementById('gif');
const question = document.getElementById('question');
const buttonsContainer = document.querySelector('.buttons');

function sayNo() {
    noCount++;
    
    // Update No button text
    const textIndex = Math.min(noCount, phrases.length - 1);
    noBtn.innerText = phrases[textIndex];
    
    // Increase Yes button size
    const currentSize = parseFloat(window.getComputedStyle(yesBtn).fontSize);
    const newSize = currentSize * 1.4;
    const currentPaddingY = parseFloat(window.getComputedStyle(yesBtn).paddingTop);
    const currentPaddingX = parseFloat(window.getComputedStyle(yesBtn).paddingLeft);
    
    yesBtn.style.fontSize = `${newSize}px`;
    yesBtn.style.padding = `${currentPaddingY * 1.2}px ${currentPaddingX * 1.2}px`;
}

function sayYes() {
    // Change GIF to happy
    gif.src = "https://media.tenor.com/_Z8Qh5A1YWEAAAAi/milk-and-mocha.gif";
    // Change text
    question.innerText = "YAAAAAAAY! I love you too! ❤️";
    // Hide buttons
    buttonsContainer.style.display = "none";
    
    // Add flying hearts
    createHearts();
}

function createHearts() {
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const heart = document.createElement('div');
            heart.innerHTML = '❤️';
            heart.style.position = 'absolute';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.top = '100vh';
            heart.style.fontSize = (Math.random() * 20 + 20) + 'px';
            heart.style.animation = `floatUp ${Math.random() * 2 + 3}s linear forwards`;
            heart.style.pointerEvents = 'none';
            heart.style.zIndex = 50;
            document.body.appendChild(heart);
            
            setTimeout(() => {
                heart.remove();
            }, 5000);
        }, i * 100);
    }
}
