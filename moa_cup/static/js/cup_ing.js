const cardLeft = document.getElementById('card-left');
const cardRight = document.getElementById('card-right');
const nextBtn = document.getElementById('next-btn');

function selectCard(selected, other) {
    selected.classList.add('selected');
    selected.classList.remove('unselected');
    other.classList.add('unselected');
    other.classList.remove('selected');
    nextBtn.disabled = false;
}

cardLeft.addEventListener('click', () => selectCard(cardLeft, cardRight));
cardRight.addEventListener('click', () => selectCard(cardRight, cardLeft));
