from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username} ({self.id})"


class List(models.Model):

    CATEGORY_CHOICES = [
       ('Fashion', 'Fashion'),
       ('Books,Movies & Music','Books,Movies & Music'),
       ('Electronics', 'Electronics'),
       ('Collectibles & Art','Collectibles & Art'),
       ('Home & Garden', 'Home & Garden'),
       ('Sporting Goods','Sporting Goods' ),
       ('Toys & Hobbies','Toys & Hobbies' ),
       ('Businness & Industrials', 'Businness & Industrials'),
       ('Health & Beauty','Health & Beauty' ),
       ('Others', 'Others'),
    ]

    item_id = models.AutoField(primary_key=True)
    title =  models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    start_bid =  models.IntegerField()
    description = models.TextField()
    img_url = models.URLField(max_length=1000)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_item")




    def __str__(self):
        return f"{self.user_id}: | {self.item_id}: {self.title}, {self.category}, {self.start_bid}, active: {self.active}"


class Bid(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid = models.IntegerField()
    item_id =  models.ForeignKey(List, on_delete=models.CASCADE, related_name="user_item")

    def __str__(self):
        return f"{self.user_id}: | {self.bid} |{self.item_id}"

class Comment(models.Model):
    item_id =  models.ForeignKey(List, on_delete=models.CASCADE, related_name="itme_comment")
    body = models.TextField()
    name = models.CharField(max_length=80)
    created_on = models.DateTimeField(auto_now_add=True)
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

    def __str__(self):
         return 'Comment: {}     / by {}'.format(self.body, self.name)



class WahchList(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watch_list")
    item_id =  models.ForeignKey(List, on_delete=models.CASCADE, related_name="itme_watch_list")

    def __str__(self):
        return f"{self.user_id} ({self.item_id})"


