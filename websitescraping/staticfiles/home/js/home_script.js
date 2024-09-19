$(document).ready(function() {

    function cleanResults() {
        resultsContainer.empty();
        scrapeTimeContainer.text('');
    }

    function showPreloader() {
        var preloaderContainer = document.getElementById('preloader-container');
        preloaderContainer.innerHTML = `
            <div class="row center-align">
                <div class="col s12 m12">
                    <div class="preloader-wrapper big active">
                        <div class="spinner-layer spinner-yellow-only">
                        <div class="circle-clipper left">
                            <div class="circle"></div>
                        </div><div class="gap-patch">
                            <div class="circle"></div>
                        </div><div class="circle-clipper right">
                            <div class="circle"></div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        preloaderContainer.style.display = 'block';
    }

    function hidePreloader() {
        var preloaderContainer = document.getElementById('preloader-container');
        preloaderContainer.style.display = 'none';
    }

    function setupInputFieldListener(inputField, clearIcon) {
        inputField.addEventListener('input', function() {
            if (inputField.value.length > 0) {
                clearIcon.style.display = 'block';
            } else {
                clearIcon.style.display = 'none';
            }
        });
    }

    function setupClearIconListener(inputField, clearIcon) {
        clearIcon.addEventListener('click', function() {
            inputField.value = '';
            clearIcon.style.display = 'none';
            inputField.focus();
        });
    }

    function setupResetButtonListener() {
        $('#reset-button').click(function() {
            cleanResults();
            resultsCardsContainer.css('visibility', 'hidden');
        });
    }

    function setupScrapeButtonListener() {
        $('#scrape-button').click(function() {
            var websiteUrl = $('#website-url').val();

            if (!websiteUrl) {
                cleanResults();
                resultsContainer.append('<p>Error: Website URL cannot be empty.</p>');
                resultsCardsContainer.css('visibility', 'visible');
                return;
            }

            if (!websiteUrl.startsWith('http://') && !websiteUrl.startsWith('https://')) {
                websiteUrl = 'https://' + websiteUrl;
            }

            var urlWithoutProtocol = websiteUrl.replace(/^https?:\/\//, '');
            if (!urlWithoutProtocol.startsWith('www.')) {
                websiteUrl = websiteUrl.replace(/^https?:\/\//, 'https://www.');
            }

            showPreloader();

            $.ajax({
                url: scrapeUrlsUrl,
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrfToken,
                    url: websiteUrl
                },
                success: function(response) {
                    cleanResults();
                    resultsContainer.append('<ul>');
                    if (response.scraped_urls) {
                        response.scraped_urls.forEach(function(url) {
                            resultsContainer.append('<li>' + url + '</li>');
                        });
                    } else {
                        resultsContainer.append('<li>No URLs found.</li>');
                    }
                    resultsContainer.append('</ul>');
                    hidePreloader();
                    scrapeTimeContainer.append('Scrape time: ' + response.hour + ' - ' + response.date);
                    resultsCardsContainer.css('visibility', 'visible');
                },
                error: function(xhr, status, error) {
                    resultsContainer.append('<p>Error: ' + error + '</p>');
                    hidePreloader();
                }
            });
        });
    }

    var inputField = document.getElementById('website-url');
    var clearIcon = document.getElementById('clear-input-icon');
    var resultsContainer = $('#results');
    var resultsCardsContainer = $('#results-cards');
    var scrapeTimeContainer = $('#scrape-time');

    setupInputFieldListener(inputField, clearIcon);
    setupClearIconListener(inputField, clearIcon);
    setupResetButtonListener();
    setupScrapeButtonListener();
});