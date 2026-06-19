document.querySelectorAll('.round_btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.round_btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
    });
});

document.querySelectorAll('.category_btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.category_btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
    });
});
