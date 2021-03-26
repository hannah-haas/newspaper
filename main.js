const logBtn = document.getElementById('explore');
logBtn.addEventListener('click', fetchData);

async function fetchData() {

    const response = await fetch('https://hannah-haas.github.io/newspaper/article_list.json');
    const data = await response.json();
    var random_article_list = []

    data.forEach(obj => {
        Object.entries(obj).forEach(([key, values]) => {

            console.log(values.keys());
            if (values.length != 0){
              random_article_list = random_article_list.concat(values)
            }

        });
    });
    console.log(random_article_list)
    random_num = Math.floor(Math.random() * Math.floor(random_article_list.length));
    random_article = random_article_list[random_num]
    console.log(random_article)
    // document.location.href = random_article

}
