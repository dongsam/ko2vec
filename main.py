#-*- coding: utf-8 -*-
# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
# sys.stdin = codecs.getreader('utf-8')(sys.stdin)
# reload(sys)
# sys.setdefaultencoding('utf-8')
import ko2vec

# def __main___():

mysql_host = "52.69.42.132"
mysql_user = "nomad"
mysql_passwd = "qlqjs123"
mysql_db = "nomad"


opinion_pos = ko2vec.loader.LoaderMysql(mysql_host,mysql_user,mysql_passwd,mysql_db)
opinion_pos.query('select sentence, 1, CONCAT(opinion_company_id, "-", opinion_id) from OPINION WHERE opinion_value > 0 ORDER BY opinion_date DESC LIMIT 10000')
opinion_pos_tagged = ko2vec.preprocesser.MecabTagging(opinion_pos)
print opinion_pos_tagged.count_tokens()
print opinion_pos_tagged.count_unique_tokens()

opinion_neg = ko2vec.loader.LoaderMysql(mysql_host,mysql_user,mysql_passwd,mysql_db)
opinion_neg.query('select sentence, 0, CONCAT(opinion_company_id, "-", opinion_id) from OPINION WHERE opinion_value < 0 ORDER BY opinion_date DESC LIMIT 10000')
opinion_neg_tagged = ko2vec.preprocesser.MecabTagging(opinion_neg)
print opinion_neg_tagged.count_tokens()
print opinion_neg_tagged.count_unique_tokens()

news_unsupervised = ko2vec.loader.LoaderMysql(mysql_host,mysql_user,mysql_passwd,mysql_db)
news_unsupervised.query("select news_content, 0, news_url from NEWS order by news_date DESC limit 1000")
news_unsupervised_tagged = ko2vec.preprocesser.MecabTagging(news_unsupervised)
print news_unsupervised_tagged.count_tokens()
print news_unsupervised_tagged.count_unique_tokens()


sources = [opinion_neg_tagged, opinion_pos_tagged]
unsupervised_sources=[news_unsupervised_tagged]
trained = ko2vec.trainer.GensimDoc2VecTrainer(sources, unsupervised_sources=unsupervised_sources, vector_size=300, epoch=20)
trained.save_model("1_1_5.model")

for i in trained.get_most_similar(u'상승/Noun'):
    print i[0], i[1]

for i in trained.model.most_similar(positive=[u'상승/Noun', u'급등/Noun'], negative=[u'하락/Noun']):
    print i[0], i[1]

trained.cross_validation(k_fold=5)


# if __name__ == '__main__':
#     __main___()




# trained.model.docvecs.offset2doctag