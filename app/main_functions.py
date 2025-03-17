def find_post(id:int,my_posts,response='post'):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            if response == 'index':
                return i
            elif response == 'post': 
                return post
    return None