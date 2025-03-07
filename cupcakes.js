$(document).ready(function () {
    // Function to fetch and display cupcakes
    function fetchCupcakes() {
      axios.get('/api/cupcakes')
        .then(response => {
          const cupcakes = response.data.cupcakes;
          const cupcakesList = $('#cupcakes-list');
          cupcakesList.empty(); // Clear the list first
  
          cupcakes.forEach(cupcake => {
            cupcakesList.append(`
              <li>
                <h3>${cupcake.flavor}</h3>
                <p>Size: ${cupcake.size}</p>
                <p>Rating: ${cupcake.rating}</p>
                <img src="${cupcake.image}" alt="${cupcake.flavor} image" width="100">
              </li>
            `);
          });
        })
        .catch(error => {
          console.error('Error fetching cupcakes:', error);
        });
    }
  
    // Function to handle form submission
    $('#new-cupcake-form').submit(function (event) {
      event.preventDefault();
  
      const newCupcake = {
        flavor: $('#form-flavor').val(),
        size: $('#form-size').val(),
        rating: $('#form-rating').val(),
        image: $('#form-image').val() || "https://tinyurl.com/demo-cupcake"
      };
  
      axios.post('/api/cupcakes', { cupcake: newCupcake })
        .then(response => {
          fetchCupcakes();  // Refresh the list
          $('#new-cupcake-form')[0].reset();  // Clear the form
        })
        .catch(error => {
          console.error('Error adding new cupcake:', error);
        });
    });
  
    // Initial fetch of cupcakes
    fetchCupcakes();
  });
  