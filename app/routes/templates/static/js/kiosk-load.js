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
          displayItems(data.kiosk_items, data.total_records, page, perPage, search);
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
  
function displayItems(items, totalPages, currentPage, perPage, search) {
    const itemsContainer = document.getElementById("itemContainer");
    const paginationContainer = document.getElementById("paginationContainer");
    itemsContainer.innerHTML = ""; // Clear existing content
    paginationContainer.innerHTML = "";
  
    if (Array.isArray(items)) {
        const rows = Math.ceil(items.length / 5);

        for (let i = 0; i < rows; i++){
            // create a rwo element
            const row = document.createElement("div");
            row.classList.add("item-row");
            row.classList.add("mt-5");
            row.style.display = "flex"; // set flexbox for horizontal alignment

            // get the number of items to display in the current row
            const itemsInRow = Math.min(5, items.length - i * 5);

            // loop element thgouth items for the current row and create item cards
            for (let j = 0; j < itemsInRow; j++) {
                const item = items[i * 5 + j]; // access item based on row 
                const itemCard = document.createElement("div");
                itemCard.classList.add("item-card");
                itemCard.classList.add("mx-3");
                const cardFlex = document.createElement("div");
                cardFlex.classList.add("d-flex");
                cardFlex.classList.add("justify-content-between");
                itemCard.appendChild(cardFlex);
                
                // image section
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("image-container");
                const image = document.createElement("img");
                image.id = "image-item";
                image.src = `static/assets/images/mall-items/${item.kiosk_detail.item_image}`;
                image.style.height = "150px";
                image.style.width = "150px";
                imageContainer.appendChild(image);
                cardFlex.appendChild(imageContainer);

                // detail section
                const details = document.createElement("div");
                details.classList.add("item-details");
                details.classList.add("mt-1")

                // Create the strong tag first and set its text content
                const strname = document.createElement("strong");
                strname.textContent = item.kiosk_detail.item_name;

                // Then create the p tag and append the strong tag to it
                const name = document.createElement("p");
                name.appendChild(strname);

                // Finally, append the entire paragraph to the details element
                details.appendChild(name);


                const price = document.createElement("p");
                price.classList.add("mb-0");
                price.textContent = `Price: ${item.kiosk_detail.item_price} Point`;
                details.appendChild(price);

                const item_category = document.createElement("p");
                item_category.classList.add("mb-0");
                item_category.textContent = `Category: ${item.kiosk_detail.item_category}`;
                details.appendChild(item_category);

                const item_stock = document.createElement("p");
                item_stock.textContent = `Available: ${item.kiosk_detail.item_stock}`;
                details.appendChild(item_stock);

                const button = document.createElement("button");
                button.classList.add("btn");
                button.classList.add("btn-primary")
                button.textContent = "Add to Cart";
                details.appendChild(button);
                itemCard.appendChild(details);
    
                row.appendChild(itemCard);
            }
            itemsContainer.appendChild(row);
        }
        // Pagination container
        paginationContainer.classList.add("mt-5");
        paginationContainer.classList.add("justify-content-center"); // Center alignment for buttons

        // Previous button
        if (currentPage > 1) {
          const prevButton = document.createElement("button"); // Use a button instead of a span for a clickable link
          prevButton.classList.add("btn");
          prevButton.classList.add("btn-primary");
          prevButton.textContent = "<"; // Use an arrow for a more typical "previous" indicator
          prevButton.addEventListener("click", () => fetchKiosk(search, currentPage - 1, perPage));
          paginationContainer.appendChild(prevButton);
        }

        // Page number indicators
        for (let i = 1; i <= totalPages / perPage; i++) {
          const pageButton = document.createElement("button");
          pageButton.classList.add("btn");
          pageButton.classList.add("page-link"); // Use page-link for non-active buttons
          pageButton.textContent = i;
          if (i === currentPage) {
            pageButton.classList.add("active");
          }
          pageButton.addEventListener("click", () => fetchKiosk(search, i, perPage));
          paginationContainer.appendChild(pageButton);
        }

        // Next button
        if (currentPage < totalPages) {
          const nextButton = document.createElement("button");
          nextButton.classList.add("btn");
          nextButton.classList.add("btn-primary");
          nextButton.textContent = "Next"; // Use an arrow for a more typical "next" indicator
          nextButton.addEventListener("click", () => fetchKiosk(search, currentPage + 1, perPage));
          paginationContainer.appendChild(nextButton);
        }

    } else {
        console.error("Unexpected data format. Expected an array of items.");
    };
};


  // Event listener to load items on window load
window.addEventListener("load", function () {
    fetchKiosk(null, 1, 10); // Initial call with default page and perPage values
});
  