function copyLink() {
    const headline = "{% if post.title %}{{ post.title|escapejs }}{% elif video.title %}{{ video.title|escapejs }}{% else %}{{ trend.title|escapejs }}{% endif %}";

    const link = window.location.href;
    const combinedText = `${headline}\n${link}`;

    const tempInput = document.createElement('textarea');
    tempInput.value = combinedText;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    const confirmation = document.getElementById('copy-confirmation');
    confirmation.classList.remove('hidden');

    const button = document.getElementById('copy-link-button');
    button.innerHTML = '<i class="fas fa-link text-xs mr-2"></i> Copied!';

    setTimeout(function() {
        confirmation.classList.add('hidden');
        button.innerHTML = '<i class="fas fa-link text-xs mr-2"></i> Copy Link';
    }, 2000);
}


document.addEventListener('DOMContentLoaded', function () {
    const shareButton = document.getElementById('share-button');
    const shareDropdown = document.getElementById('share-dropdown');

    shareButton.addEventListener('click', function () {
        shareDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', function (event) {
        if (!shareButton.contains(event.target) && !shareDropdown.contains(event.target)) {
            shareDropdown.classList.add('hidden');
        }
    });

    const contentContainer = document.getElementById("contentContainer");
    const fontChangeButton = document.getElementById("fontChangeButton");
    const textSizeChangeButton = document.getElementById("textSizeChangeButton");

    const fonts = ["Poppins", "Roboto", "Arial", "Georgia", "Helvetica", "Times New Roman"];
    let currentFontIndex = 0;

    const textSizes = ["text-sm", "text-base", "text-lg", "text-xl"];
    let currentTextSizeIndex = 1;

    fontChangeButton.addEventListener("click", function () {
        currentFontIndex = (currentFontIndex + 1) % fonts.length;
        contentContainer.style.fontFamily = fonts[currentFontIndex];
    });

    textSizeChangeButton.addEventListener("click", function () {
        textSizes.forEach(size => contentContainer.classList.remove(size));
        currentTextSizeIndex = (currentTextSizeIndex + 1) % textSizes.length;
        contentContainer.classList.add(textSizes[currentTextSizeIndex]);
    });

    const fontSizeChangeText = document.getElementById("fontSizeChangeText");
    const textSizeChangeText = document.getElementById("textSizeChangeText");

    fontChangeButton.addEventListener("mouseenter", function () {
        fontSizeChangeText.classList.remove("hidden");
    });

    fontChangeButton.addEventListener("mouseleave", function () {
        fontSizeChangeText.classList.add("hidden");
    });

    textSizeChangeButton.addEventListener("mouseenter", function () {
        textSizeChangeText.classList.remove("hidden");
    });

    textSizeChangeButton.addEventListener("mouseleave", function () {
        textSizeChangeText.classList.add("hidden");
    });
});