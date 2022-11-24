from django.http import JsonResponse, HttpRequest

from posts.models import Post


async def cpu(request: HttpRequest):
    """High cpu route
    CPU: High
    I/O: low
    """
    ct = 0
    for i in range(10**7):
        ct += i * i
    return JsonResponse({"ct": ct})


async def io_create(request: HttpRequest):
    """Create 1 post
    CPU: low
    I/O: High
    """
    new_post = await Post.objects.acreate(
        title=request.POST["title"],
        content=request.POST["content"],
    )
    return JsonResponse(new_post.to_dict())


async def io_read(request: HttpRequest):
    """Get first 25 posts
    CPU: low
    I/O: High
    """
    posts = []
    async for p in Post.objects.all()[:25]:
        posts.append(p)
    ct = await Post.objects.acount()
    return JsonResponse(
        {
            "ct": ct,
            "posts": [post.to_dict() for post in posts],
        }
    )
