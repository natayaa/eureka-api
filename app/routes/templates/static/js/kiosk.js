async function call_kiosk(search=null, page=1, perPage=10) {
    try {
        let url = `/application/api/v1/routes/kiosk/item_malls?page=${page}&perpage=${perPage}`;
        if (search !== null) {
            url = `/application/api/v1/routes/kiosk/item_malls?search=${search}&page=${page}&perpage=${perPage}`;
        }
        
        // Extract access token from cookie
        const cookies = document.cookie;
        
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Cookie": cookies
            },
        });

        if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data.kiosk_items)){
                // panggil html ?
                kiosk_items(items=data.kiosk_items, totalPages=data.total_records,
                    page, perPage, search)
            }
        }
    } catch(error) {
        console.log(error);
    }
}


// Function to create a single item card
function createItemCard(item) {
    const itemCard = document.createElement("div");
    itemCard.classList.add("card", "shadow", "mx-3");
    itemCard.style.maxWidth = "320px"; // Set maximum width for larger screens
    itemCard.style.width = "100%"; // Set width to 100% for responsiveness
    itemCard.style.borderRadius = "15px";

    // Create div for item image
    const imageDiv = document.createElement("div");
    imageDiv.classList.add("text-center");
    imageDiv.style.backgroundColor = "transparent";
    imageDiv.style.borderRadius = "15px";

    // Create image element
    const itemImage = document.createElement("img");
    itemImage.id = `itemImageShow_${item.kiosk_detail.item_id}`;
    itemImage.src = `static/assets/images/mall-items/${item.kiosk_detail.item_image}`;
    itemImage.style.width = "100%";
    itemImage.style.maxWidth = "100%"; // Adjust maximum width for responsiveness

    // listen for the error
    itemImage.addEventListener("error", function() {
        const placeholderImage = new Image();
        placeholderImage.onload = function () {
            itemImage.src = "static/assets/images/no-image.png";
            itemImage.style.width = "100%";
            itemImage.style.maxWidth = "100%"; // Adjust maximum width for responsiveness
        };
        placeholderImage.onerror = function() {
            //
        }
        placeholderImage.src = "static/assets/images/no-image.png";
        placeholderImage.style.width = "100%";
        placeholderImage.style.maxWidth = "100%"; // Adjust maximum width for responsiveness
    })

    // Append image to image div
    imageDiv.appendChild(itemImage);

    // Append image div to item card
    itemCard.appendChild(imageDiv);

    // Create footer div for item details
    const footerDiv = document.createElement("div");
    footerDiv.style.backgroundColor = "transparent";
    footerDiv.classList.add("card-footer", "border-top", "border-gray-300", "p-4", "text-center");

    // Create elements for item name, description, price, and purchase button
    const itemName = document.createElement("a");
    itemName.href = "#";
    itemName.classList.add("h5");
    itemName.id = `${item.kiosk_detail.item_name}`;
    itemName.textContent = item.kiosk_detail.item_name;
    itemName.style.fontSize = "1.2em"; // Responsive font size

    const itemDescription = document.createElement("h3");
    itemDescription.classList.add("h6", "fw-light", "text-gray", "mt-2");
    itemDescription.id = "item_description";
    itemDescription.textContent = item.kiosk_detail.item_desc;
    itemDescription.style.fontSize = "1em"; // Responsive font size

    const itemStock = document.createElement("h3");
    itemStock.classList.add("h6", "fw-light", "text-gray", "mt-2");
    itemStock.textContent = `Stock: ${item.kiosk_detail.item_stock}`;
    itemStock.style.fontSize = "1em";

    const itemPrice = document.createElement("div");
    itemPrice.classList.add("d-flex", "justify-content-between", "align-items-center", "mt-3");

    const spanPrice = document.createElement("span");
    spanPrice.classList.add("h5", "mb-0", "text-grey");
    spanPrice.id = "item_price";
    spanPrice.textContent = `${item.kiosk_detail.item_price} Point`;
    spanPrice.style.fontSize = "1em"; // Responsive font size

    const buttonBuy = document.createElement("button");
    buttonBuy.id = `buyItem_${item.mall_id}`;
    buttonBuy.classList.add("btn", "btn-xs", "btn-primary");

    const buyIconButton = document.createElement("span");
    buyIconButton.classList.add("bi", "bi-bag-heart-fill");
    buyIconButton.textContent = "Purchase";

    buttonBuy.appendChild(buyIconButton);

    // Append elements to item price div
    itemPrice.appendChild(spanPrice);
    itemPrice.appendChild(buttonBuy);

    // Append elements to footer div
    footerDiv.appendChild(itemName);
    footerDiv.appendChild(itemDescription);
    footerDiv.appendChild(itemStock);
    footerDiv.appendChild(itemPrice);

    // Append footer div to item card
    itemCard.appendChild(footerDiv);

    return itemCard;
}


// Function to display items in rows
function displayItemRows(items) {
    const itemsContainer = document.getElementById("itemContainer");
    itemsContainer.classList.add("mb-5");
    itemsContainer.innerHTML = "";
    const rows = Math.ceil(items.length / 4);

    for (let i = 0; i < rows; i++) {
        const row = document.createElement("div");
        row.classList.add("item-row", "mt-5", "mb-5");
        row.style.display = "flex";

        const itemsInRow = Math.min(4, items.length - i * 4);

        for (let card = 0; card < itemsInRow; card++) {
            const item = items[i * 4 + card];
            const itemCard = createItemCard(item);
            row.appendChild(itemCard);
        }

        itemsContainer.appendChild(row); // Append row to body or any desired parent element
    }
}

// Function to create pagination controls
function createPagination(totalPages, currentPage, search, perPage) {
    const paginationContainer = document.createElement("nav");
    paginationContainer.setAttribute("aria-label", "Page navigation example");

    const paginationList = document.createElement("ul");
    paginationList.classList.add("pagination");

    // Previous button
    const previousButton = document.createElement("li");
    previousButton.classList.add("page-item");
    const previousLink = document.createElement("a");
    previousLink.classList.add("page-link");
    previousLink.textContent = "Previous";
    previousLink.href = "#";
    previousLink.addEventListener("click", () => {
        if (currentPage > 1) {
            call_kiosk(search, currentPage - 1, perPage);
        }
    });
    previousButton.appendChild(previousLink);
    paginationList.appendChild(previousButton);

    // Page numbers
    for (let i = 1; i <= Math.ceil(totalPages / perPage); i++) {
        const pageItem = document.createElement("li");
        pageItem.classList.add("page-item");
        const pageLink = document.createElement("a");
        pageLink.classList.add("page-link");
        pageLink.textContent = i;
        pageLink.addEventListener("click", () => {
            call_kiosk(search, i, perPage);
        });
        if (i === currentPage) {
            pageItem.classList.add("active");
        }
        pageItem.appendChild(pageLink);
        paginationList.appendChild(pageItem);
    }

    // Next button
    const nextButton = document.createElement("li");
    nextButton.classList.add("page-item");
    const nextLink = document.createElement("a");
    nextLink.classList.add("page-link");
    nextLink.textContent = "Next";
    nextLink.addEventListener("click", () => {
        if (currentPage < totalPages) {
            call_kiosk(search, currentPage + 1, perPage);
        }
    });
    nextButton.appendChild(nextLink);
    paginationList.appendChild(nextButton);

    paginationContainer.appendChild(paginationList);

    return paginationContainer;
}


// Main function to display items in kiosk
async function kiosk_items(items, totalPages, currentPage, perPage, search) {
    try {
        // Call function to display item rows
        displayItemRows(items);

        // Call function to create pagination controls
        const paginationControls = createPagination(totalPages, currentPage, search, perPage);
        const paginationContainer = document.getElementById("paginationContainer");
        paginationContainer.innerHTML = "";
        paginationContainer.appendChild(paginationControls);
    } catch(error) {
        console.error(error);
        // Handle error here
    }
}

window.addEventListener("load", function() {
    call_kiosk(search=null, page=1, perPage=12);
})
