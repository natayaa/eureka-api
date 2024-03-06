async function fetchKiosk(search = null, page = 1, perPage = 10) {
    try {
      let url = `/application/api/v1/routes/kiosk/item_malls?page=${page}&perpage=${perPage}`;
      console.log("Fetching data from:", url);
  
      if (search !== null) {
        url = `/application/api/v1/routes/kiosk/item_malls?search=${search}&page=${page}&perpage=${perPage}`;
      }
  
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Accept": "application/json",
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Received data:", data);
  
        if (Array.isArray(data.kiosk_items)) {
          displayItems(data.kiosk_items);
        } else {
          console.error("Unexpected data format. Expected an array of items.");
        }
      } else {
        console.error(`Error fetching data: ${response.status}`);
        // Handle specific errors based on error type (e.g., NetworkError)
        throw new Error(`Failed to fetch data. Please try again later.`);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      // Provide more specific error messages to the user based on error type
      throw error;
    }
  }
  
function displayItems(items) {
    const itemsContainer = document.getElementById("itemContainer");
    itemsContainer.innerHTML = ""; // Clear existing content
  
    if (Array.isArray(items)) {
        const rows = Math.ceil(items.length / 5);

        for (let i = 0; i < rows; i++){
            // create a rwo element
            const row = document.createElement("div");
            row.classList.add("item-row");
            row.style.display = "flex"; // set flexbox for horizontal alignment

            // get the number of items to display in the current row
            const itemsInRow = Math.min(5, items.length - i * 5);

            // loop element thgouth items for the current row and create item cards
            for (let j = 0; j < itemsInRow; j++) {
                const item = items[i * 5 + j]; // access item based on row 
                const itemCard = document.createElement("div");
                itemCard.classList.add("item-card");
    
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("image-container");
                const image = document.createElement("img");
                image.src = `static/assets/images/mall-items/${item.kiosk_detail.item_image}`;
                image.style.height = "150px";
                image.style.width = "150px";
                imageContainer.appendChild(image);
                itemCard.appendChild(imageContainer);
    
                const details = document.createElement("div");
                details.classList.add("item-details");
                const name = document.createElement("h3");
                name.textContent = item.kiosk_detail.item_name;
                details.appendChild(name);
                const price = document.createElement("p");
                price.textContent = `Price: Rp.${item.kiosk_detail.item_price.toFixed(2)}`;
                details.appendChild(price);
                const button = document.createElement("button");
                button.textContent = "Add to Cart";
                details.appendChild(button);
                itemCard.appendChild(details);
    
                row.appendChild(itemCard);
            }
            itemsContainer.appendChild(row);
        }
    } else {
        console.error("Unexpected data format. Expected an array of items.");
    };
};
  
  // Event listener to load items on window load
window.addEventListener("load", function () {
    fetchKiosk(null, 1, 10); // Initial call with default page and perPage values
});
  