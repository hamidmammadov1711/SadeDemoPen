// script.js
console.log('CTF Lab Frontend çalışıyor');
function submitFlag() {
  const flag = document.getElementById("flag").value;
  fetch("http://localhost:8000/check_flag", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({flag: flag})
  }).then(res => res.json()).then(data => alert(data.message));
}

