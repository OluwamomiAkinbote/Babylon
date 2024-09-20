document.getElementById('search-input').addEventListener('input', function() {
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
                        document.getElementById('search-input').value = item;
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

// Close the suggestion box when clicking outside
document.addEventListener('click', function(e) {
    var suggestionBox = document.getElementById('suggestion-box');
    if (!document.getElementById('search-input').contains(e.target)) {
        suggestionBox.classList.add('hidden');
    }
});