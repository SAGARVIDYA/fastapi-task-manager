let token = ""


async function register(){

let username = document.getElementById("reg_user").value

let password = document.getElementById("reg_pass").value


await fetch("http://127.0.0.1:8000/register",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

username,

password

})

})


alert("registered")

}



async function login(){

let username = document.getElementById("login_user").value

let password = document.getElementById("login_pass").value


let res = await fetch("http://127.0.0.1:8000/login",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

username,

password

})

})


let data = await res.json()

token = data.access_token


alert("login success")

loadTasks()

}



async function createTask(){

let title = document.getElementById("task_title").value

let description = document.getElementById("task_desc").value


await fetch("http://127.0.0.1:8000/tasks",{

method:"POST",

headers:{

"Content-Type":"application/json",

"Authorization":"Bearer " + token

},

body:JSON.stringify({

title,

description

})

})


loadTasks()

}



async function loadTasks(){


let res = await fetch("http://127.0.0.1:8000/tasks",{

headers:{

"Authorization":"Bearer " + token

}

})


let data = await res.json()


document.getElementById("tasks").innerHTML = data.map(t =>

`

<li>

${t.title} - ${t.completed}

<button onclick="deleteTask(${t.id})">Delete</button>

</li>

`

).join("")

}



async function deleteTask(id){


await fetch("http://127.0.0.1:8000/tasks/"+id,{

method:"DELETE",

headers:{

"Authorization":"Bearer " + token

}

})


loadTasks()

}