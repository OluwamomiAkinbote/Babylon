document.addEventListener('DOMContentLoaded', function () {
  const mediaInput = document.querySelector('input[type="file"][name$="media"]');  // Target the media file input field
  const previewElement = document.querySelector('.field-preview .readonly');

  if (mediaInput && previewElement) {
      mediaInput.addEventListener('change', function () {
          const file = mediaInput.files[0];
          if (file) {
              const reader = new FileReader();
              reader.onload = function (e) {
                  const fileURL = e.target.result;
                  previewElement.innerHTML = `<img src="${fileURL}" width="100" height="100" style="object-fit: cover;" />`;
              };
              reader.readAsDataURL(file);
          }
      });
  }
});
