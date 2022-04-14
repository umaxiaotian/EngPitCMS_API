import array
from ast import dump
from multiprocessing.dummy import Array
from click import echo
from models.article import Article
from models.user import User
from cruds.auth import *

# 一般ユーザー　記事リスト取得
def getArticleList():
    # 記事情報を取得
    query = Article.select().get()
    articles = []
    for article in query.select().order_by(Article.good_count.desc()).limit(10):
        relate_user_name = User.get(article.relate_user_id).name
        articles.append(
            {"relate_user_id": article.relate_user_id, "relate_user_name": relate_user_name, "title": article.title, "good_count": article.good_count, "tags": article.tags, "post_date": article.post_date})

    return articles

# 一般ユーザー　記事内容取得
def getArticleDetail(article_id: int):
    article = Article.get(article_id)
    relate_user_name = User.get(article.relate_user_id).name
    return {"relate_user_id": article.relate_user_id, "relate_user_name": relate_user_name, "title": article.title, "detail": article.detail, "good_count": article.good_count, "tags": article.tags, "post_date": article.post_date}


# 会員ページ＿自身の記事リスト
def getMyArticleList(user_id: User = Depends(get_current_user)):
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.relate_user_id == user_id).order_by(Article.post_date.desc()):
        relate_user_name = User.get(article.relate_user_id).name
        articles.append(
            {"relate_user": article.relate_user_id, "relate_user_name": relate_user_name,  "title": article.title, "detail": article.detail, "good_count": article.good_count, "tags": article.tags, "post_date": article.post_date})

    return articles

