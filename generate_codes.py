def format_text1(name):
    return f"""
      {name}: {{
        handler () {{
          console.log('{name} changed!');
          localStorage.setItem('{name}', JSON.stringify(this.{name}));
        }},
        deep: true
      }},
    """.rstrip("\n ")

text = """data: data.list,
        qIndex: 0,
        activeIndex: -1,
        rightIndex: -1,
        errorIndex: -1,
        questionList: [],
        ansState: false,
        collectionList: [],
        collectHtmlData: [],
        collectNum: 0,
        errorHtmlData: [],
        errNum: 0,
        collectionState: false,
        collectionText: '收藏',
        toast: false,
        toastText: '',
        allQuestionState: []"""

print('\n'*10)
for name in text.split('\n'):
    name = name.split(':')[0].strip()
    print(format_text1(name))



def format_text2(name):
    return f"""
      if (localStorage.getItem('{name}')) this.{name} = JSON.parse(localStorage.getItem('{name}'));
""".rstrip("\n")

print('\n'*10)
for name in text.split('\n'):
    name = name.split(':')[0].strip()
    print(format_text2(name))
