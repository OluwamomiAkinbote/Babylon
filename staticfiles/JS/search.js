// Variables for the timeout
let searchTimeout;
const searchTimeoutDuration = 10000; // 10 seconds before auto-hide

// Toggle search bar visibility on mobile
document.getElementById('search-toggle').addEventListener('click', function() {
    var searchContainer = document.getElementById('search-container');
    
    // Show the search container
    searchContainer.classList.remove('hidden');
    searchContainer.classList.add('flex'); // Ensure it's flex for layout
    
    // Focus on input and start auto-hide timeout
    document.getElementById('mobile-search-input').focus();
    searchTimeout = setTimeout(hideSearchContainer, searchTimeoutDuration);
});

// Cancel the search with the cancel button
document.getElementById('search-cancel').addEventListener('click', function() {
    hideSearchContainer();
});

// Hide the search container after timeout
function hideSearchContainer() {
    var searchContainer = document.getElementById('search-container');
    searchContainer.classList.remove('flex');
    searchContainer.classList.add('hidden');
    clearTimeout(searchTimeout); // Clear any active timeout
}

// Handle search input and suggestions
document.getElementById('mobile-search-input').addEventListener('input', function() {
    var query = this.value;

    if (query.length > 0) {
        fetch(`/get-suggestions/?query=${query}`)
            .then(response => response.json())
            .then(data => {
                var suggestionBox = document.getElementById('suggestion-box');
                suggestionBox.innerHTML = ''; // Clear previous suggestions
                suggestionBox.classList.remove('hidden'); // Show the box

                if (data.length > 0) {
                    data.forEach(function(item) {
                        var suggestionItem = document.createElement('div');
                        suggestionItem.classList.add('p-2', 'hover:bg-gray-100', 'cursor-pointer');
                        suggestionItem.innerHTML = item;

                        // Add click event to select the suggestion
                        suggestionItem.addEventListener('click', function() {
                            document.getElementById('mobile-search-input').value = item;
                            suggestionBox.classList.add('hidden'); // Hide suggestions after selection
                        });

                        suggestionBox.appendChild(suggestionItem);
                    });
                } else {
                    var noResult = document.createElement('div');
                    noResult.classList.add('p-2', 'text-gray-500');
                    noResult.innerHTML = 'No results found';
                    suggestionBox.appendChild(noResult);
                }
            });
    } else {
        document.getElementById('suggestion-box').classList.add('hidden');
    }
});

// Close suggestion box when clicking outside
document.addEventListener('click', function(e) {
    var suggestionBox = document.getElementById('suggestion-box');
    var searchInput = document.getElementById('mobile-search-input');

    if (!searchInput.contains(e.target) && !suggestionBox.contains(e.target)) {
        suggestionBox.classList.add('hidden');
    }
});
