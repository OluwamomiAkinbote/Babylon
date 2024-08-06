
    document.addEventListener('DOMContentLoaded', function() {
        updatePostDates('.post-date');  // Initialize date updating

        setInterval(function() {
            updatePostDates('.post-date');  // Update dates every second
        }, 1000);
    });

    function updatePostDates(selector) {
        var postDates = document.querySelectorAll(selector);
        console.log('Updating post dates for elements:', postDates); // Debugging output
        postDates.forEach(function(postDate) {
            var dateElement = postDate.getAttribute('data-date');
            console.log('Original data-date attribute:', dateElement); // Debugging output
            var date = new Date(parseInt(dateElement) * 1000);  // Convert UNIX timestamp to milliseconds
            var currentDate = new Date();
            var secondsAgo = Math.floor((currentDate - date) / 1000);

            if (secondsAgo < 60) {
                postDate.textContent = secondsAgo + ' seconds ago';
            } else if (secondsAgo < 3600) {
                var minutesAgo = Math.floor(secondsAgo / 60);
                postDate.textContent = minutesAgo + ' minutes ago';
            } else if (secondsAgo < 86400) {
                var hoursAgo = Math.floor(secondsAgo / 3600);
                postDate.textContent = hoursAgo + ' hours ago';
            } else {
                // Default to the original date format if more than 24 hours ago
                postDate.textContent = date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
            }
            console.log('Updated post date text:', postDate.textContent); // Debugging output
        });
    }

