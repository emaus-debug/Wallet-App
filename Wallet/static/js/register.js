const username = document.querySelector('#username');
const feedBackArea = document.querySelector('.invalid_feedback');
const email = document.querySelector('#email');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');
const password = document.querySelector('#password');
const showPasswordToggle = document.querySelector('.showPasswordToggle');

const handleToggleInput = (e)=>{
    if(showPasswordToggle.textContent === "voir"){
        showPasswordToggle.textContent = "masquer";

        password.setAttribute("type", "text");
    }
    else{
        showPasswordToggle.textContent = "voir";

        password.setAttribute("type", "password");
    }
}

showPasswordToggle.addEventListener("click", handleToggleInput);

email.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    email.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0){
        fetch('/authapp/validate-email', 
        {
            body : JSON.stringify({ email: emailVal }),
            method : "POST",
            headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, 
        }).then((res) =>res.json())
        .then((data)=>{
            console.log('data',data);
            if (data.email_error){
                email.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = data.email_error
            }
        });
    }
});

username.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    username.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0){
        fetch('/authapp/validate-username', 
        {
            body : JSON.stringify({ username: usernameVal }),
            method : "POST",
            headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, 
        }).then((res) =>res.json())
        .then((data)=>{
            console.log('data',data);
            if (data.username_error){
                username.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = data.username_error
            }
        });
    }
});