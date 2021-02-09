// Splitting the form elements into pages
var currentPage = 0;
showPage(currentPage);

function showPage(number) {
    var pages = document.getElementsByClassName("page");
    pages[number].style.display = "block";

    if (number == 0) {
        document.getElementById("previous_button").style.display = "none";
    } else {
        document.getElementById("previous_button").style.display = "inline";
    }
    if (number == (pages.length - 1)) {
        document.getElementById("next_button").innerHTML = "Submit";
    } else {
        document.getElementById("next_button").innerHTML = "Next";
    }
}

function nextPrev(number) {
    var pages = document.getElementsByClassName("page");

    pages[currentPage].style.display = "none";
    currentPage = currentPage + number;
    if (currentPage >= pages.length) {
        document.getElementById("form").submit();
        return false;
    }
    showPage(currentPage);
}