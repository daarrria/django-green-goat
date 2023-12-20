(function () {
    const header = document.querySelector('header');
    window.onscroll = () => {
        if (window.pageYOffset > 60) {
            header.classList.add('header_active');
        } else {
            header.classList.remove('header_active');
        }
    };
}());


function updateRangeValue(sliderId, inputId) {
    var sliderValue = document.getElementById(sliderId).value;
    document.getElementById(inputId).value = sliderValue;
  }

  function applyFilters() {
    var priceMin = document.getElementById('price_min').value;
    var priceMax = document.getElementById('price_max').value;
    console.log('Price Min:', priceMin);
    console.log('Price Max:', priceMax);
  }