import re
import os

base_dir = os.path.dirname(os.path.realpath('__file__'))


def parse_all():
    results = []
    for page in range(1, 66):
        path = os.path.join(base_dir, 'contents/{:0>3}.htm'.format(page))
        with open(path, 'r') as f:
            res = f.read()

            p = re.compile(r'\w，?\s*字\w{2}')
            result = p.findall(res)
            result = [r for r in result if not r.startswith('小字')]
            results += result
    return results


def parse_page(page):
    path = os.path.join(base_dir, 'contents/{:0>3}.htm'.format(page))
    with open(path, 'r') as f:
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
    first_names = read_first_names()

    names = []
    for page in range(1, 2):
        content, results = parse_page(page)
        soup = BeautifulSoup(content, "html.parser")
        text = soup.find("div", id="main").get_text()
        text = text.replace('\n', '')
        print('{:-^30}'.format(page))
        cuts = jieba.cut(text)

        for result in results:
            index = text.index(result)
            pattern = re.compile(r'.\w' + result[0])
            possible_names = pattern.findall(text, index - 300, index + 1)
            result = result.replace('，', '')
            result_name = result.split('字')
            result_name.insert(0, None)
            print(possible_names)
            for index, possible_name in enumerate(possible_names):
                print(possible_name)
                if possible_name[:-1] in first_names:
                    continue
                if possible_name[1] in first_names:
                    possible_names[index] = possible_name[1:]
                    continue
                possible_names.remove(possible_name)
            possible_names = list(set(possible_names))
            if len(possible_names) == 1:
                result_name[0] = possible_names[0][0]
                print(result_name[0])
            print(result_name)
            names.append(result_name)

    print(len(names))   # 513
    names = [name for name in names if name[0]]
    print(len(names))   # 903

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
