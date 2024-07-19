
def get_address(category):
    titles = []
    while category:
            titles.append(category.name)
            category = category.sub_category
    titles.sort()
    return  " / ".join(titles)