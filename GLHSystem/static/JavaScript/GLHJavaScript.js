//Provided the search bar function
function overallSiteSearchFunction() {
  var input = document.getElementById("search-bar-input");
  var filter = input.value.toUpperCase();
  var items = document.getElementsByClassName("product-item");
  for (let item of items) {
    var txtValue = item.textContent || item.innerText;

    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      item.style.display = "";
    } else {
      item.style.display = "none";
    }
  }
}
function hideAllergenFilter(){
    document.querySelector(".collapsible-filter-content").classList.toggle("hide-filter-mode");
}

//Prevents the page from refreshing which resets the allergen filter
document.getElementById("search-bar-input").addEventListener("input", function(e) {
    e.preventDefault();
    overallSiteSearchFunction();
});

document.querySelector(".product-filter-button").addEventListener("click", hideAllergenFilter);

//Toggles the delivery box on cechkout page
function hideDeliveryBox() {
    document.getElementById('delivery-address-box').classList.toggle("hide-filter-mode");
    if (delivery.checked) {
        box.classList.add("hide-filter-mode");
    } else {
        box.classList.remove("hide-filter-mode");
    }}