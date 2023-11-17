

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


 // Js Script for Product review

 const stars = document.querySelectorAll('.star-for-review');
 let starSelectedValue = 0;


 stars.forEach(star => {
     star.addEventListener('mouseover', function() {
         const starId = parseInt(star.id);
         for (let i = 1; i <= starId; i++) {
             document.getElementById(i.toString()).classList.add('checked');
         }
     });
 
     star.addEventListener('mouseout', function() {
         if (starId !== starSelectedValue) {
             stars.forEach(s => {
                 s.classList.remove('checked');
             });
         }
     });
 
     star.addEventListener('click', function() {

        for (let i = 1; i <= 5; i++) {
            document.getElementById(i.toString()).classList.remove('checked');
        }

         starSelectedValue = parseInt(star.id);
         for (let i = 1; i <= starSelectedValue; i++) {
             document.getElementById(i.toString()).classList.add('checked');
         }
         // You can now use the 'starSelectedValue' variable to send to the database
        //  console.log('Selected value:', starSelectedValue);
     });
 });
 


// getting the submit button and CLICK event
const submitButton = document.getElementById('submit-review-button')
// submitButton.addEventListener('click',submitProductReview(3,4))

submitButton.addEventListener('click', function() {
    var productReviewText = document.getElementById('customer-review').value;
    // console.log('submit click')
    // console.log(productReviewText)
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    var productId = document.getElementById('product-id').value;
    // console.log(productId)
    var xhr = new XMLHttpRequest()

    xhr.onload = function (){
        var response = xhr.responseText;
        // console.log(response)
    }
    xhr.open(
        'POST',
        '/add-product-review/',
        csrf_token[0].value
    )
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrf_token[0].value);
    var data = {
        'stars': starSelectedValue,
        'review_messages':productReviewText,
        'product_id':productId
    }

    xhr.send(JSON.stringify(data))
 });


