const categories = document.querySelectorAll('.category');

categories.forEach(cat => {
    cat.addEventListener('click', () => {
        // 기존 선택 해제
        categories.forEach(c => c.classList.remove('selected'));
        // 클릭한 것만 선택
        cat.classList.add('selected');
    });
});