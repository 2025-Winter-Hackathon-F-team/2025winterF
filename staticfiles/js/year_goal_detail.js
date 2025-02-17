// 年目標の編集切り替え
function toggleEdit() {
  let displayDiv = document.getElementById("year-goal-display");
  let formDiv = document.getElementById("year-goal-form");

  if (displayDiv.style.display === "none") {
    displayDiv.style.display = "block";
    formDiv.style.display = "none";
  } else {
    displayDiv.style.display = "none";
    formDiv.style.display = "block";
  }
}

// CSRFトークンを取得する関数
function getCsrfToken() {
  let csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
  return csrfTokenElement ? csrfTokenElement.value : "";
}

// 年目標の保存処理
function saveGoal(year) {
  let newTitle = document.getElementById("goal-input").value;
  let csrfToken = getCsrfToken(); // CSRFトークンを取得

  fetch(`/goal/year_goal/${year}/edit/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ title: newTitle, year: year }),
  })
    .then((response) =>
      response.json().then((data) => ({ status: response.status, body: data }))
    )
    .then(({ status, body }) => {
      if (status === 200) {
        console.log("Success:", body.message);
        document.getElementById("year-goal-text").textContent = newTitle;
        document.getElementById("error-message").textContent = "";
        toggleEdit();
      } else {
        // バリデーションエラーを投げる
        throw body.error;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("error-message").textContent = error.title
        ? error.title.join(", ")
        : "保存に失敗しました";
    });
}