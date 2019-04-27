
# coding: utf-8

# In[1]:


import re
from bs4 import BeautifulSoup


# In[2]:


def printlist(l):
    for e in l:
        print(e)
        print('-'*12)


# In[3]:


id = 0
Big_Data = []


# In[36]:
for superindex in range(1,10):
    with open(f"{str(superindex)}.html", 'r') as f:
        htmlDoc = f.read()
    print(htmlDoc)


    # In[37]:


    soup = BeautifulSoup(htmlDoc, 'html.parser')


    # In[38]:


    result = soup.find_all("div", class_="quesBox")
    type(result)


    # In[39]:


    def clean0(text):
        return re.sub(r'\d+、\s+', '', question).strip()

    def clean1(text):
        return text.lstrip("1234567890. 󰃆、 ").strip(' ')

    def clean2(text):
        if (text in ["正确", "错误"]) or len(text) <= 2:
            return text
        r = text[2:].strip(' ').strip("󰃆、")
        if r[0] == '.':
            r = '0' + r
        return r

    def change(text):
        #text = text.replace('.', '、')
        text = text.replace("（", "(").replace("）", ")")
        try:
            text = re.sub(r'\(.*\)', re.findall(r'\(.*\)', text)[0].replace(" ", ''), text)
        except Exception as e:
            print(e)
            print('wroung at change')
        text = text.replace('()', '(   )')
        return text


    # In[40]:


    data_list = []
    #    {
    #      "id": 1,
    #      "title": "驾驶技能准考证明的有效期是多久？",
    #      "items": [
    #        "1年",
    #        "2年",
    #        "3年",
    #        "4年"
    #      ],
    #      "answer": 1,
    #      "reason": "驾驶技能准考证明的有效期为三年，申请人应当在有效期内完成科目二和科目三考试。未在有效期内完成考试的，已考试合格的科目成绩作废。"
    #    },
    for i in result:
        try:
            temp_dict = {}
            id += 1
            question = i.find_all("div", attrs={"class":"quesTitle"})[0].get_text()
            question = clean0(question)
            print(question)
            ABCD = ['', '', '', '', '']
            try:
                right_answer= i.find_all("div", attrs={"correct": "True"})[0].get_text()
            except Exception as e:
                print(e)
                right_answer= i.find_all("div", attrs={"correct": "true"})[0].get_text()
            right_answer = clean1(right_answer)
            right_answer_index = -1
            for index, each_ans in enumerate(i.find_all("div", attrs={"class": 'answer'})):
                ABCD[index] = clean1(each_ans.get_text())
                print(clean1(each_ans.get_text()))
                if right_answer == ABCD[index]:
                    right_answer_index = index
            if right_answer_index == -1:
                continue
            temp_dict = {
                "id": id,
                "title": change(question),
                "items": [
                    clean2(ABCD[0]),
                    clean2(ABCD[1]),
                    clean2(ABCD[2]),
                    clean2(ABCD[3])
                ],
                "answer": right_answer_index,
                "reason": ""
            }
            data_list.append(temp_dict)
        except Exception as e:
            print(e)
            #input("continus?")



    # In[57]:


    Big_Data += data_list


# In[24]:


final_data = {'list': Big_Data}


# In[25]:


import json

text = json.dumps(final_data)

with open('data.json', 'w', encoding='utf-8') as f:
    f.write(text)

