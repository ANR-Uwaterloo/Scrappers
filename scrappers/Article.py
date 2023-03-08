class Article(object):
    """
    Class representing a single news article containing all the information that news-please can extract.
    """
    authors = []
    publish_date = None
    description = None
    img_url = None
    link = None
    category = None
    headline = None

    def get_dict(self):
        """
        Article object
        """
        return {
            'authors': self.authors,
            'description': self.description,
            'img_url': self.img_url,
            'category': self.category,
            'headline': self.headline,
            'link': self.link,
            'publish_date': self.publish_date,
        }