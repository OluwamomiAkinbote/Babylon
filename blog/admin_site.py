# blog/admin_site.py
from django.contrib.admin import AdminSite

class SportsAdminSite(AdminSite):
    site_header = 'Sports Admin'
    site_title = 'Sports Admin Portal'
    index_title = 'Manage Sports Posts'

class GlobalNewsAdminSite(AdminSite):
    site_header = 'Global News Admin'
    site_title = 'Global News Admin Portal'
    index_title = 'Manage Global News Posts'

class CentralAdminSite(AdminSite):
    site_header = 'Central Admin'
    site_title = 'Central Admin Portal'
    index_title = 'Manage All Posts'

sports_admin_site = SportsAdminSite(name='sports_admin')
global_news_admin_site = GlobalNewsAdminSite(name='global_news_admin')
central_admin_site = CentralAdminSite(name='central_admin')
