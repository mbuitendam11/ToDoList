
function priorityLevel() {
    let priority = document.getElementById("priority");
    if (priority == "1") {
        return priority.innerHTML = "Urgent";
    } else if (priority == "2") {
        return priority.innerHTML = "High";
    } else if (priority == "3") {
        return priority.innerHTML = "Medium";
    } else if (priority == "4") {
        return priority.innerHTML = "Low";
    } else {
        return priority.innerHTML = "Something went wrong!";
    }
}

