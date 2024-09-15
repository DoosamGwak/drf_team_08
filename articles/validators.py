from .models import Article,Comment

def get_article(pk):
    try:
        return Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return None
    

def get_comment(pk):
    try:
        return Comment.objects.get(pk=pk,is_deleted=False)
    except Comment.DoesNotExist:
        return None