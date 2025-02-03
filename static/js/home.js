// ユーザー情報を取得
const user = "{{user.lifespan_end_date}}";
console.log(user);

console.log("home.js is loaded!");
// 寿命カウントダウン
function showRestTime(user) {
  console.log(user);
  console.log("ああああ！");
  const now = new Date(); //現在時刻を取得する
  // const lifespan_end = new Date(2050, 0, 1);
  const lifespan_end_str =
    document.querySelector("div.time-box").dataset.lifespanEnd;
  const lifespan_end = new Date(lifespan_end_str);

  console.log("lifespan_end:", lifespan_end);

  //指定した日付までの残り時間をミリ秒で取得する ※割ってミリ秒→秒→分→時間→日数に変換、小数点以下切り捨て
  const restMillisecond = lifespan_end.getTime() - now.getTime();
  const day = Math.floor(restMillisecond / 1000 / 60 / 60 / 24);
  const hour = Math.floor(restMillisecond / 1000 / 60 / 60) % 24;
  const minute = Math.floor(restMillisecond / 1000 / 60) % 60;
  const second = Math.floor(restMillisecond / 1000) % 60;

  document.getElementById("day").textContent = day;
  document.getElementById("hour").textContent = hour;
  document.getElementById("minute").textContent = String(minute).padStart(
    2,
    "0"
  );
  document.getElementById("second").textContent = String(second).padStart(
    2,
    "0"
  );
}

// 指定したミリ秒ごとに関数を実行する
setInterval(showRestTime, 1000);
