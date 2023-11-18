
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

