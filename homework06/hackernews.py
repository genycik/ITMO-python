from bottle import route, run, template, request, redirect
import bottle
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import sqlalchemy
import string

bottle.TEMPLATE_PATH.insert(0, '')

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows = rows)


@route("/add_label/")
def add_label():
    s = session()
    news_item = s.query(News).filter(News.id == request.query.id).one()
    news_item.label = request.query.label
    s.commit() 
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    hot_news = get_news("https://news.ycombinator.com/newest", n_pages=32)
    db_news = s.query(News).all()
    db_title_author = [(news_item.title, news_item.author) for news_item in db_news]
    for latest_news in hot_news:
        if (latest_news['title'], latest_news['author']) not in db_title_author:
            news = News(title = latest_news['title'],
                author = latest_news['author'], 
                url = latest_news['url'], 
                comments = latest_news['comments'], 
                points = latest_news['points'], 
                )

            s.add(news)
        s.commit()


    redirect("/news")

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier.fit(x_train, y_train)

    rows = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for row in rows:
        prediction = classifier.predict([clean(row.title)])
        if prediction == 'good':
            good.append(row)
        elif prediction == 'maybe':
            maybe.append(row)
        else:
            never.append(row)

    return template('recommended', good=good, maybe=maybe, never=never)


if __name__ == "__main__":
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier = NaiveBayesClassifier()
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
