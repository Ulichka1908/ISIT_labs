function loadXML() {
    let level2Index = document.getElementById("level2-number").value;
    level2Index = parseInt(level2Index) - 1; 
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "films.xml", true); 
    
    xhr.onload = function() {
        if (xhr.status == 200) {
            var xmlDoc = xhr.responseXML;
            
            var movies = xmlDoc.getElementsByTagName("movie");
            
            if (level2Index >= movies.length) {
                alert("Неверный номер второго уровня.");
                return;
            }

            var selectedMovie = movies[level2Index];

            var titles = selectedMovie.getElementsByTagName("title");
            var durations = selectedMovie.getElementsByTagName("duration");
            var genres = selectedMovie.getElementsByTagName("genre");
            var ratings = selectedMovie.getElementsByTagName("rating");

            var outputDiv = document.getElementById("output");
            outputDiv.innerHTML = ""; 
            
            for (var i = 0; i < titles.length; i++) {
                outputDiv.innerHTML += `<p>Название: ${titles[i].textContent}</p>`;
                outputDiv.innerHTML += `<p>Длительность: ${durations[i].textContent}</p>`;
                outputDiv.innerHTML += `<p>Жанр: ${genres[i].textContent}</p>`;
                outputDiv.innerHTML += `<p>Рейтинг: ${ratings[i].textContent}</p>`;
                outputDiv.innerHTML += "<hr>";
            }
        } else {
            alert("Ошибка загрузки XML: " + xhr.status);
        }
    };

    xhr.onerror = function() {
        alert("Произошла ошибка при запросе XML.");
    };

    xhr.send(); 
}
