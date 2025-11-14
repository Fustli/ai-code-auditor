// Example JavaScript code with common issues

var users = []; // Should use const/let instead of var

function addUser(username, password) {
    // No input validation
    var user = {
        id: users.length + 1,
        username: username,
        password: password, // Security: plain text password
        createdAt: new Date()
    };
    users.push(user);
    return user;
}

// Performance: inefficient array search
function findUser(username) {
    for (var i = 0; i < users.length; i++) {
        if (users[i].username === username) {
            return users[i];
        }
    }
    return null;
}

// Security: vulnerable to XSS
function displayMessage(message) {
    document.getElementById('output').innerHTML = message;
}

// Quality: missing error handling
function processData(data) {
    var result = data.split(',');
    return result.map(function(item) {
        return parseInt(item);
    });
}

// Performance: blocking operation without async
function fetchDataFromAPI() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/data', false); // Synchronous request
    xhr.send();
    return JSON.parse(xhr.responseText);
}