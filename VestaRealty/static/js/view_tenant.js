document.addEventListener('DOMContentLoaded',() =>{
    
    const deleteButtons = document.querySelectorAll('button[data-id]');

    deleteButtons.forEach(button =>{
        button.addEventListener('click',(event) =>{
            event.preventDefault();
            const button_ = event.target.closest('button');
            const tenant_id = button_.getAttribute('data-id');
            
            const row = event.target.closest('tr');

            if(confirm('Are you sure you want to Delete all records on this tenant,This action is irreversible?')){
                // ajax request
                $.ajax({
                    url:`/delete-tenant/${tenant_id}/`,
                    method:'DELETE',
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(), // Get CSRF token from form
                        'Content-Type': 'application/json'
                    },
                    success:function(response){
                        row.remove();

                        // Add Toast here
                        Toastify({
                            text: "Tenant blablabla has been deleted.",
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
                    error: (xhr,status,error) =>{
                        console.error("Error:   ",error);
                        // add toast here
                        Toastify({
                            text: "An error has occurred.Please try again.",
                            duration: 3000,
                            newWindow: true,
                            close: true,
                            gravity: "top", // `top` or `bottom`
                            position: "center", // `left`, `center` or `right`
                            stopOnFocus: true, 
                            style: {
                              background: "red",
                            },
                          }).showToast();
                    }

                });
            }
        });
    });
});