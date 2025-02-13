var $btn = document.getElementById("submit");
var $form = document.getElementById("form");

function login() {
  if ($form.checkValidity()) {
    $btn.classList.add("pending");
    window.setTimeout(function () {
      $btn.classList.add("granted");
    }, 1500);
  }
}

$btn.addEventListener("click", year_goal_create);
