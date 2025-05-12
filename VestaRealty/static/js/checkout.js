document.addEventListener('DOMContentLoaded',()=>{


    //form submission
    const form = document.getElementById('checkout_form');

    form.addEventListener('submit',(event) =>{
        event.preventDefault();

        const form_data = new FormData(event.target);

        if(confirm('Proceed to Payment?')){
            // ajax submission 
            $.ajax({
                type: 'POST',
                url: '/checkout',
                data: form_data,
                processData: false,
                contentType: false,
                success: function(response, status, xhr) {
                    console.log("Status:", status);
                    // console.log("Full response:", response);
                    console.log("Content-Type:", xhr.getResponseHeader('Content-Type'));
                    // toast notification
                    Toastify({
                        text: "Payment has been Processed,Please wait for the MPESA message.Thank You.",
                        duration: 3000,
                        newWindow: true,
                        close: true,
                        gravity: "top", // `top` or `bottom`
                        position: "center", // `left`, `center` or `right`
                        stopOnFocus: true, 
                        style: {
                            background: "green",
                        },
                        }).showToast();

                },
                error: function(error) {
                    console.error('Error:', error);

                    Toastify({
                            text: "Please Try Again.",
                            duration: 3000,
                            newWindow: true,
                            close: true,
                            gravity: "top", // `top` or `bottom`
                            position: "center", // `left`, `center` or `right`
                            stopOnFocus: true, 
                            style: {
                              background: "green",
                            },
                          }).showToast();
                }
            });

            form.reset();
        }
    });
});