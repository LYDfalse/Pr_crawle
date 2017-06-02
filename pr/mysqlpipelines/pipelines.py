from .sql import Sql
from pr.items import PrItem



class PrPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, PrItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print('已经存在了')
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.insert_dd_name(xs_name, xs_author, category, name_id)
                print('开始存小说标题')
        if isinstance(item, PrItem):
            url = item['chapterurl']
            name_id = item['id_name']
            num_id = item['num']
            xs_chaptername = item['chaptername']
            xs_content = item['chapterconten']
            Sql.insert_dd_chaptername(xs_chaptername, xs_content, name_id, num_id, url)
            print('小说存储完毕')
            return item