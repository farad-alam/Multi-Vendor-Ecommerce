

function change_cart_quantity(cart_id,values) {
    // console.log(typeof(cart_id))
    // console.log(typeof(values))

    var xhr = new XMLHttpRequest()

    xhr.onload= function() {
        var response = xhr.responseText
         console.log(typeof(response['total_product_price']))
         console.log(response['total_product_price'])
         console.log(typeof(response['sub_total']))
         response = JSON.parse(response)
         var jsonResponse = response['carts_product']
        //  console.log(jsonResponse)
        let formatteTortalProductPrice = response['total_product_price'].toFixed(2);
        let formattedSubTotal   = response['sub_total'].toFixed(2);
         document.getElementById('product-quantity-'+cart_id).innerText = response['product_quantity']
         document.getElementById('total_product_price-'+cart_id).innerText = '$'+ formatteTortalProductPrice
         document.getElementById('sub_total_price').innerText = '$'+ formattedSubTotal 

         // Get the table element to append product rows
        var table = document.querySelector('table');



        if ( jsonResponse.length > 0) {

            if ( jsonResponse[0] === 'no-product'){
                
                // Get the table element to append product rows
                var table = document.querySelector('table');            

                // Clear the existing table
                while (table.firstChild) {
                    table.removeChild(table.firstChild);
                }
                return;
                
            }

            // Get the table element to append product rows
            var table = document.querySelector('table');            

            // Clear the existing table
            while (table.firstChild) {
                table.removeChild(table.firstChild);
            }
            // Loop through the JSON response and create a row for each product
            jsonResponse.forEach(function(product, index) {
                var row = document.createElement('tr');
                
                var thumbnailCell = document.createElement('td');
                thumbnailCell.className = 'product-thumbnail';
                var thumbnailLink = document.createElement('a');
                thumbnailLink.href = 'shop-details.html';
                var thumbnailImage = document.createElement('img');
                thumbnailImage.src = product.image;
                thumbnailImage.alt = '';
                thumbnailLink.appendChild(thumbnailImage);
                thumbnailCell.appendChild(thumbnailLink);
                
                var nameCell = document.createElement('td');
                nameCell.className = 'product-name';
                var nameLink = document.createElement('a');
                nameLink.href = 'shop-details.html';
                nameLink.textContent = product.title;
                nameCell.appendChild(nameLink);
                
                var priceCell = document.createElement('td');
                priceCell.className = 'product-price';
                var priceSpan = document.createElement('span');
                priceSpan.className = 'amount';
                priceSpan.textContent = '$' + product.regular_price;
                priceCell.appendChild(priceSpan);
                var quantityCell = document.createElement('td');
                quantityCell.className = 'product-quantity';
            
                var quantityDiv = document.createElement('div');
                quantityDiv.className = 'd-inline-flex';
            
                var minusButton = document.createElement('div');
                minusButton.className = 'btn btn-outline-info minus';
                minusButton.textContent = '-';
                minusButton.onclick = function() {
                change_cart_quantity(product.id, 2);
                };
            
                var quantityP = document.createElement('p');
                quantityP.className = 'mx-2 cart-quantity';
                quantityP.id = 'product-quantity-' + product.id;
                quantityP.textContent = product.quantity;
            
                var plusButton = document.createElement('div');
                plusButton.className = 'btn btn-outline-info plus-' + product.id;
                plusButton.textContent = '+';
                plusButton.onclick = function() {
                change_cart_quantity(product.id, 1);
                };

                var subtotalCell = document.createElement('td');
                subtotalCell.className = 'product-subtotal';
                var subtotalSpan = document.createElement('span');
                subtotalSpan.className = 'amount';
                subtotalSpan.textContent = '$'+product.total_product_price;
                subtotalCell.appendChild(subtotalSpan);
            
                var removeCell = document.createElement('td');
                removeCell.className = 'product-remove';
                var removeLink = document.createElement('a');
                removeLink.href = '#';
                removeLink.onclick = function() {
                  change_cart_quantity(product.id, 0);
                }
                var removeIcon = document.createElement('i');
                removeIcon.className = 'fa fa-times';
                removeLink.appendChild(removeIcon);
                removeCell.appendChild(removeLink);
            
                
                // Add the cells to the row
                row.appendChild(thumbnailCell);
                row.appendChild(nameCell);
                row.appendChild(priceCell);

                quantityDiv.appendChild(minusButton);
                quantityDiv.appendChild(quantityP);
                quantityDiv.appendChild(plusButton);
            
                quantityCell.appendChild(quantityDiv);
                row.appendChild(quantityCell);
                row.appendChild(subtotalCell);
                row.appendChild(removeCell);

                // Append the row to the table
                table.appendChild(row);
            });

        }


    }

    xhr.open(
        'POST',
        '/increse-cart/'
    )

    var data ={
        "id":cart_id,
        'values': values
    }

    xhr.send(JSON.stringify(data))

}




