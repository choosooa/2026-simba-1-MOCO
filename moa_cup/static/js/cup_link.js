const linkText = document.querySelector('.link_text');
const copyIcon = document.querySelector('.copy_icon');
const copyBtn = document.querySelector('.copy_btn');

function copyLink() {
    navigator.clipboard.writeText(linkText.textContent.trim());
}

copyIcon.addEventListener('click', copyLink);
copyBtn.addEventListener('click', copyLink);
