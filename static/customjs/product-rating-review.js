

document.addEventListener('DOMContentLoaded', function() {
    const allReviewStars = document.querySelectorAll('.stars-number'); // Fetch the number of stars from Django template

    allReviewStars.forEach(reviewStars => {
        // console.log('all star review foreach')
        // console.log(reviewStars.value.split("-"))
        const reviewStarsNumber = reviewStars.value.split("-")[0]
        const reviewStarsId = reviewStars.value.split("-")[1]

        // Add stars based on reviewStarsNumber
        for (let i = 0; i < reviewStarsNumber; i++) {
            var starsContainer = document.getElementById('str-info-'+reviewStarsId)
            const star = document.createElement('a');
            star.href = '#';
            star.innerHTML = '<i class="fas fa-star"></i>';
            starsContainer.appendChild(star);
        }

        // Calculate the number of additional stars needed to reach a total of 5
        const additionalStars = 5 - reviewStarsNumber;

        // Add additional stars if needed
        for (let i = 0; i < additionalStars; i++) {
        var starsContainer = document.getElementById('str-info-'+reviewStarsId)
        const star = document.createElement('span');
        // star.href = '#';
        // star.innerHTML = '<span class="fa fa-star" ></span>';
        star.classList.add('fa', 'fa-star')
        starsContainer.appendChild(star);
        }

    });

 } );

 

 // GETING STAR from user

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
          const starId = parseInt(star.id);
         if (starId !== starSelectedValue ) {
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
 

// GETING REVIEW AND SAVE TO DATA BASE

// getting the submit button and CLICK event
const submitButton = document.getElementById('submit-review-button')
// submitButton.addEventListener('click',submitProductReview(3,4))

submitButton.addEventListener('click', function() {
    var productReviewText = document.getElementById('customer-review').value;
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    var productId = document.getElementById('product-id').value;
    var xhr = new XMLHttpRequest()

    xhr.onload = function (){
        // var response = xhr.responseText;
        // console.log(response)

        // Empty the text area
        document.getElementById('customer-review').value = '';

        // Remove selecting star after submiting the review
        stars.forEach(star => {
            star.classList.remove('checked');           
            });

        // Display a notification for 3 seconds after submission
        var notification = document.querySelector('.notification');
        notification.textContent = 'Your review was submitted';
        notification.style.display = 'block';

        setTimeout(function() {
            notification.style.display = 'none';
        }, 4000);
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

