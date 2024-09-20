        // Function to toggle the visibility of the navbar based on screen width
        function toggleNavbarVisibility() {
            const navbar = document.querySelector('.navbar');
            if (window.innerWidth < 657) {
                navbar.style.display = 'none';
            } else {
                navbar.style.display = 'flex';
            }
        }
    
        // Initial check
        document.addEventListener('DOMContentLoaded', toggleNavbarVisibility);
    
        // Check on window resize
        window.addEventListener('resize', toggleNavbarVisibility);
    
        // Toggle category container visibility
        document.getElementById('menu-button').addEventListener('click', function () {
            let categoryContainer = document.getElementById('category-container');
            categoryContainer.classList.toggle('hidden');
        });
    
        // Toggle search container visibility
        document.getElementById('search-toggle').addEventListener('click', function () {
            let searchContainer = document.getElementById('search-container');
            searchContainer.classList.toggle('hidden');
        });


  document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('mobile-search-button');
    const searchInput = document.getElementById('mobile-search-input');
    const suggestionList = document.getElementById('search-suggestions');
    
    // Function to fetch and update suggestions
    function updateSuggestions(query) {
        if (query.length > 0) {
            fetch(`/get-suggestions/?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionList.innerHTML = ''; // Clear previous suggestions

                    if (data.length > 0) {
                        data.forEach(function (item) {
                            const option = document.createElement('option');
                            option.value = item;
                            suggestionList.appendChild(option);
                        });
                    }
                });
        } else {
            suggestionList.innerHTML = ''; // Clear suggestions when query is empty
        }
    }

    // Update suggestions on input
    searchInput.addEventListener('input', function () {
        const query = this.value;
        updateSuggestions(query);
    });

    // Perform search on button click
    searchButton.addEventListener('click', function () {
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/search/?query=${encodeURIComponent(query)}`;
        }
    });
});