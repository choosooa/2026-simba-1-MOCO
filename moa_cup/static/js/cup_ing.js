const cardLeft = document.getElementById('card-left');
const cardRight = document.getElementById('card-right');
const nextBtn = document.getElementById('next-btn');
const backBtn = document.querySelector('.back-btn');
const exitModal = document.querySelector('.Frame158');
const modalCancel = document.getElementById('modal-cancel');
const modalConfirm = document.getElementById('modal-confirm');
const screen = document.querySelector('.screen');

function selectCard(selected, other) {
    selected.classList.add('selected');
    selected.classList.remove('unselected');
    other.classList.add('unselected');
    other.classList.remove('selected');
    nextBtn.disabled = false;
}

cardLeft.addEventListener('click', () => selectCard(cardLeft, cardRight));
cardRight.addEventListener('click', () => selectCard(cardRight, cardLeft));

nextBtn.addEventListener('click', () => {
    window.location.href = nextBtn.dataset.url;
});

backBtn.addEventListener('click', (e) => {
    e.preventDefault();
    exitModal.classList.add('active');
    screen.classList.add('modal-open');
});

modalCancel.addEventListener('click', () => {
    exitModal.classList.remove('active');
    screen.classList.remove('modal-open');
});

modalConfirm.addEventListener('click', () => {
    window.location.href = modalConfirm.dataset.url;
});
