document.getElementById('search-form').addEventListener('submit', function(event) {
    var idValue = document.getElementById('id').value;
    var keywordValue = document.getElementById('palabra_clave').value;
    if (!idValue && !keywordValue) {
        document.getElementById('search-warning').style.display = 'block';
        event.preventDefault(); 
    } else {
        document.getElementById('search-warning').style.display = 'none';
    }
});

document.getElementById('clear-button').addEventListener('click', function() {
    document.getElementById('id').value = '';
    document.getElementById('palabra_clave').value = '';
    document.getElementById('search-form').submit();
});
