#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from future_builtins import *
from ngram import NGram
import psycopg2
import sys
import codecs

class MainClass:

  def main():

    # NGramで解析する単位の設定
    index = NGram(N=2)
    list_recruit = []
    count = [0] * 10
    # projects_hit_count = [[count_hits,id]]
    projects_hit_count = []

    # DB
    connector = psycopg2.connect(host="localhost",database="wantedly")
    cursor    = connector.cursor()

    # 質問読み込み
    print "質問："
    input_q = raw_input().decode("utf-8")
    for input_q in index.ngrams(index.pad(input_q)):

        # 入力されたメッセージを含まれたものを全て出すため
        input_q = "%"+input_q+"%"

        # SQL
        sql="select id,company_id,title,description,location,keywords from projects where looking_for like '%s'"%input_q

        # print sql
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
          count[row[0]] = count[row[0]] +1

    for i in range(0,10):
      if count[i] != 0:
        projects_hit_count.append([count[i],i])

    # ヒット数高い順
    projects_hit_count.sort()
    projects_hit_count.reverse()
    print projects_hit_count

    if len(projects_hit_count) ==0:
      a=0
      #　当てはめる募集がなかった場合
      print "やりたい仕事がありますか？それか興味ある分野とは？"
    elif len(projects_hit_count) < 3:
      a=len(projects_hit_count)
      print "\nこんにちは、今のような募集がありますが、いかがですか？"
    else:
      a=3
      print "\nこんにちは、今のような募集がありますが、いかがですか？"

    for i in range(0,a):
      sql="select id,company_id,title,description,location,keywords from projects where id ='%s'"%projects_hit_count[i][1]

      # print sql
      cursor.execute(sql)
      result = cursor.fetchall()
      for row in result:
        print str(i+1)+"."
        print str(row[2])
        print str(row[5])


    connector.commit()

    cursor.close()
    connector.close()


  if __name__ == "__main__":
    main()

a = MainClass()
