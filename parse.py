import re


def parse_all():
    results = []
    for page in range(1, 66):
        page = '{:0>3}'.format(page)

        with open('{0}.htm'.format(page), 'r') as f:
            res = f.read()

            p = re.compile(r'\w，?\s*字\w{2}')
            result = p.findall(res)
            print(result)
            result = [r for r in result if not r.startswith('小字')]
            results += result
    return results


def parse_page(page):
    page = '{:0>3}'.format(page)

    with open('{0}.htm'.format(page), 'r') as f:
        content = f.read()

        p = re.compile(r'\w，?\s*字\w{2}\W')
        results = p.findall(content)
        results = [result[:-1]
                   for result in results if not result.startswith('小字')]
    return content, results


def read_first_names():
    with open('first_names.txt', 'r') as f:
        lines = f.read().splitlines()
    names = []
    for line in lines:
        if not line:
            continue
        names += line.strip()
    return names


if __name__ == '__main__':
    from bs4 import BeautifulSoup
    import jieba
    import json
    first_names = read_first_names()

    a = []
    for page in range(1, 2):
        content, results = parse_page(page)
        soup = BeautifulSoup(content, "html.parser")
        text = soup.find("div", id="main").get_text()
        text = text.replace('\n', '')
        print('{:-^30}'.format(page))
        cuts = jieba.cut(text)
        with open('a.json', 'w') as f:
            bb = list(cuts)
            f.write(json.dumps(bb, indent=4))

        for result in results:
            index = text.index(result)
            p = re.compile(r'.\w' + result[0])
            names = p.findall(text, index - 300, index + 1)
            result = result.replace('，', '')
            b = result.split('字')
            b.insert(0, None)
            print(names)
            for index, name in enumerate(names):
                print(name)
                if name[:-1] in first_names:
                    continue
                if name[1] in first_names:
                    names[index] = name[1:]
                    continue
                names.remove(name)
            names = list(set(names))
            if len(names) == 1:
                b[0] = names[0][0]
                # print(names[0])
            else:
                for b1 in bb:
                    if len(b1) > 1 and b1.endswith(b[1]):
                        print(b1)
                # for first_name in first_names:
                #     name = first_name + b[1]
                #     p = re.compile(name)
                #     r = p.findall(content)
                #     if r:
                #         print(r)
            print(b)
            a.append(b)

    q = [i for i in a if i[0]]
    print(len(q))   # 513
    print(len(a))   # 903

    # 父子弟兄
    # 复姓
    # 諱

    # content, results = parse_page(1)
    # # print(results)
    # i = 0
    # for first_name in first_names:
    #     for result in results:
    #         name = first_name + result[0]
    #         p = re.compile(name)
    #         r = p.findall(content)
    #         if r:
    #             i += 1
    #             print(name, p.findall(content))
    # print(len(results))
    # print(i)
