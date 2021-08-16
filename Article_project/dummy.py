from app_article.models import ArticleModel
# Create your tests here.
def AuthorFilter():
    qs = ArticleModel.objects.all()
    print(qs)
    #return render(request,'article/author_filter.html',{'data':object})
AuthorFilter()