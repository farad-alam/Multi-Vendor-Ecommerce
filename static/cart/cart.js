
function increase(params) {
    console.log(typeof(params))

    var xhr = new XMLHttpRequest()

    xhr.onload= function() {
        var response = xhr.responseText
         console.log(response)
        }

    xhr.open(
        'POST',
        '/increse-cart/'
    )


    var data ={
        "id":params
    }

    xhr.send(JSON.stringify(data))

}




