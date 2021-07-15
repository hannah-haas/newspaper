const logBtn = document.getElementById('explore');
logBtn.addEventListener('click', fetchData);

async function fetchData() {

  const response = await fetch('https://hannah-haas.github.io/newspaper/article_list.json');
  const data = await response.json();
  var random_article_list = []

  data.forEach(obj => {
    Object.entries(obj).forEach(([key, values]) => {
      values.forEach(obj => {
        Object.entries(obj).forEach(([key, values]) => {
          random_article_list = random_article_list.concat(key)
        });
      });
    });
  });
  random_num = Math.floor(Math.random() * Math.floor(random_article_list.length));
  random_article = random_article_list[random_num]
  var url = "https://hannah-haas.github.io/newspaper/" + random_article
  console.log(url)
  document.location.href = url

}