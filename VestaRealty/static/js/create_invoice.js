document.addEventListener("DOMContentLoaded",(event) => {
    event.preventDefault();
    console.log('Capturing DOMContentLoaded event');

    const success_message = document.getElementById('success_message');
    const error_message = document.getElementById('error_message');

    // get the Rent for the customer
    document.getElementById('Customer').addEventListener('change',(event) =>{
        event.preventDefault();

        let data = {
            'customer':event.target.value,
        }

        $.ajax({
            type:'POST',
            url: '/get_rent',
            data:JSON.stringify(data),
            contentType:'application/json',
            success: function(response){
                if (response.status === 'success'){
                    document.getElementById('rent').innerHTML = "Ksh" + response.Rent;
                }
            },
            error:function(error){
                console.error(error);
                
            },
        });
    });
    
    const form = document.getElementById('form');
    form.addEventListener('submit', function(event){
        event.preventDefault();
        const form_Data = new FormData(event.target)
        console.log(form_Data);

        
        $.ajax({
            type: 'POST',
            url: '/create_invoice',
            data: form_Data,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(response);
                if (response.status === 'success') {
                    console.log('success');
                        success_message.style.display = 'flex';
                        error_message.style.display = 'none';
                    setTimeout(() => {
                        success_message.style.display = 'none';
                        error_message.style.display = 'none';

                        // window.location.href = '/view_invoice';
                    }, 3000);
                    
                } else {
                    console.log(response.message);
                    
                    success_message.style.display = 'none';
                    error_message.style.display = 'flex';

                    setTimeout(() => {
                        success_message.style.display = 'none';
                        error_message.style.display = 'none';
                    }, 3000);
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });

        form.reset();
    
       

    });
});