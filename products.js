// Function to calculate the
// Jaro Similarity of two strings
// from https://www.geeksforgeeks.org/jaro-and-jaro-winkler-similarity/
function jaro_distance(s1, s2) {
    // If the strings are equal
    if (s1 == s2) return 1.0;

    // Length of two strings
    let len1 = s1.length,
        len2 = s2.length;

    if (len1 == 0 || len2 == 0) return 0.0;

    // Maximum distance upto which matching
    // is allowed
    let max_dist = Math.floor(Math.max(len1, len2) / 2) - 1;

    // Count of matches
    let match = 0;

    // Hash for matches
    let hash_s1 = new Array(s1.length);
    hash_s1.fill(0);
    let hash_s2 = new Array(s2.length);
    hash_s2.fill(0);

    // Traverse through the first string
    for (let i = 0; i < len1; i++) {
        // Check if there is any matches
        for (let j = Math.max(0, i - max_dist); j < Math.min(len2, i + max_dist + 1); j++)
            // If there is a match
            if (s1[i] == s2[j] && hash_s2[j] == 0) {
                hash_s1[i] = 1;
                hash_s2[j] = 1;
                match++;
                break;
            }
    }

    // If there is no match
    if (match == 0) return 0.0;

    // Number of transpositions
    let t = 0;

    let point = 0;

    // Count number of occurrences
    // where two characters match but
    // there is a third matched character
    // in between the indices
    for (let i = 0; i < len1; i++)
        if (hash_s1[i] == 1) {
            // Find the next matched character
            // in second string
            while (hash_s2[point] == 0) point++;

            if (s1[i] != s2[point++]) t++;
        }
    t /= 2;

    // Return the Jaro Similarity
    return (match / len1 + match / len2 + (match - t) / match) / 3.0;
}

// Jaro Winkler Similarity
function jaroWinklerSimilarity(s1, s2) {
    let jaro_dist = jaro_distance(s1, s2);

    // If the jaro Similarity is above a threshold
    if (jaro_dist > 0.7) {
        // Find the length of common prefix
        let prefix = 0;

        for (let i = 0; i < Math.min(s1.length, s2.length); i++) {
            // If the characters match
            if (s1[i] == s2[i]) prefix++;
            // Else break
            else break;
        }

        // Maximum of 4 characters are allowed in prefix
        prefix = Math.min(4, prefix);

        // Calculate jaro winkler Similarity
        jaro_dist += 0.1 * prefix * (1 - jaro_dist);
    }
    return jaro_dist.toFixed(6);
}

/**
 * Updates the list of games based on the current search filter and sort type.
 *
 * @return {void}
 */
function updateList() {
    const filter = $('#search').val().toLowerCase();
    const elems = Array.from(document.querySelectorAll('#gamesList li'));
    const sortType = $('#sort').val();

    // sort by selected sort type
    elems.sort(function (a, b) {
        if (sortType === 'alphabetical') {
            return a.textContent.localeCompare(b.textContent);
        } else if (sortType === 'reverse') {
            return b.textContent.localeCompare(a.textContent);
        }
    });

    // then filter items with the search input
    elems.forEach(function (item) {
        let similarity = jaroWinklerSimilarity(filter, item.innerHTML.toLowerCase().slice(0, filter.length - 1));
        if (item.getAttribute('aliases')) {
            for (alias in item.getAttribute('aliases').split(',')) {
                if (alias.length > 1) {
                    console.log('alias');
                    console.log(alias);
                    console.log(typeof alias);
                    console.log(alias.length);
                    similarity += jaroWinklerSimilarity(filter, alias.toLowerCase().slice(0, filter.length - 1));
                }
            }
        }

        if ((similarity >= 0.7 && item.innerHTML.length > 2) || item.innerHTML.toLowerCase().indexOf(filter) > -1) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });

    // now sort by jaro winkler distance
    elems.sort(function (a, b) {
        let distanceA = jaroWinklerSimilarity(filter, a.textContent.toLowerCase());
        if (a.getAttribute('aliases')) {
            for (alias in a.getAttribute('aliases').split(',')) {
                distanceA += jaroWinklerSimilarity(filter, alias.toLowerCase());
            }
        }

        let distanceB = jaroWinklerSimilarity(filter, b.textContent.toLowerCase());
        if (b.getAttribute('aliases')) {
            for (alias in b.getAttribute('aliases').split(',')) {
                distanceB += jaroWinklerSimilarity(filter, alias.toLowerCase());
            }
        }
        return distanceA - distanceB;
    });

    // then fill it with the sorted and filtered list
    for (const item of elems) {
        document.getElementById('gamesList').appendChild(item);
        updateGameList();
    }
}
$('#search').on('input', updateList);
$('#sort').on('change', updateList);
