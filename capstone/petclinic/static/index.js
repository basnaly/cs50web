
document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#time-slot').style.display = "none";
    document.querySelector('#submit-visit').style.display = "none";

    document.querySelector('#show-times').onclick = function () {

        const pet = document.querySelector('#pet').value;
        const type_visit = document.querySelector('#type_visit').value;
        const date_visit = document.querySelector('#date_visit').value;

        fetch(`/get_times_for_visit?pet=${pet}&type_visit=${type_visit}&date_visit=${date_visit}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.message) {
                document.querySelector('#message').innerHTML = data.message
            }
            else {
                for (let i = 0; i < data.busy_times.length; i++) {
                    const time = data.busy_times[i].time_visit;
                    if (document.getElementById(`${time}`) !== null) {
                        document.getElementById(`${time}`).disabled = true;
                    }
                }   
            }
            document.querySelector('#show-times').style.display = "none";    
            document.querySelector('#time-slot').style.display = "block";  
            document.querySelector('#submit-visit').style.display = "block";
        })
        .catch(error => {
            console.log('Error', error)
        })
        return false;
    }

    document.querySelector('#submit-visit').onclick = function () {

        const pet = document.querySelector('#pet').value;
        const type_visit = document.querySelector('#type_visit').value;
        const date_visit = document.querySelector('#date_visit').value;
        const time_visit = document.querySelector('input[name="time_visit"]:checked').value;

        fetch(`save_visit?pet=${pet}&type_visit=${type_visit}&date_visit=${date_visit}&time_visit=${time_visit}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
                document.querySelector('#message').innerHTML = data.message
                setTimeout(() => {
                    document.querySelector('#message').innerHTML = '';
                    window.location.replace("/");
                }, 3000)    
        })
        .catch(error => {
            console.log('Error', error)
        })
        return false;
    }
});