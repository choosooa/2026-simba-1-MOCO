const startBtn = document.querySelector('.start_btn');

function updateStartBtn() {
    const category = document.getElementById('selected_category').value;
    const size = document.getElementById('selected_size').value;
    startBtn.disabled = !(category && size);
}

document.querySelectorAll('.round_btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.round_btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');

        document.getElementById('selected_size').value = btn.dataset.size;
        updateStartBtn();
    });
});

document.querySelectorAll('.category_btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.category_btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');

        document.getElementById('selected_category').value = btn.dataset.categoryId;
        updateStartBtn();
    });
});