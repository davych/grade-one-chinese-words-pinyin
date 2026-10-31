"""Regression checks against the supplied textbook photos, without dependencies."""
import json
import unittest
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/words.json').read_text(encoding='utf-8'))
STROKES = json.loads((ROOT / 'data/strokes.json').read_text(encoding='utf-8'))

# Independently transcribed character rows, in the order visible in the photos.
READING_ROWS = [
    ['天地人你我他', '一二三四五上下', '口耳目手足站坐', '日月山川水火田禾', '六七八九十'],
    ['爸妈', '大马路土', '本学校班级姓名王'],
    ['哥弟画花', '打棋积木', '字词句子', '桌纸读书', '鱼鸭乌鸦', '午星期语文数写会'],
    ['白菜西瓜果', '小桥流柳', '开雪夜色美', '蓝云草原', '冰自行车', '晚昨今明个这去年'],
    ['秋气了树叶黄片从来飞', '江南可采莲戏间东北', '的家鸡竹牙用几步没参加', '鸟说是春青蛙夏着皮地就冬', '男女关正反先后内外'],
    ['对歌雨风虫清绿桃红', '力尖尘众双林森不条心金', '包尺作业笔刀宝贝少课早', '升国旗中们声起多么向立', '老师工厂医院生门卫'],
    ['船弯儿两头在里看见闪', '影前常黑狗左右它好朋友', '件有和做也办到又才能', '爷奶叔姐妹'],
    ['比尾巴谁长短把伞兔最公', '喝只处找着许石出法放进高', '点数彩半空问回答方久更长', '牛羊爪元拼音'],
]
WRITING_ROWS = [
    ['一二三上', '口耳目手', '日火田禾', '六七八十'],
    ['九王'], ['午下'], ['个去'],
    ['了子大人', '可叶东西', '竹马牙用几', '四小鸟是天', '女开关先'],
    ['云雨虫山水', '力男土木心', '尺本刀不少', '中五风立正', '工厂门卫'],
    ['月儿头里见', '在我左右', '和也又才', '爸妈'],
    ['比巴长公', '只多办石出', '来半你有', '牛羊爪白'],
]


def items(mode):
    return [item for group in DATA[mode + 'Groups'] for lesson in group['lessons'] for item in lesson['items']]


class TextbookChecks(unittest.TestCase):
    def test_rows_match_photos_and_garden_boundaries(self):
        for mode, expected in [('reading', READING_ROWS), ('writing', WRITING_ROWS)]:
            groups = DATA[mode + 'Groups']
            self.assertEqual(len(groups), 8)
            self.assertEqual([g['id'] for g in groups], [f'garden-{n}' for n in range(1, 9)])
            actual = [[''.join(i['char'] for i in lesson['items']) for lesson in g['lessons']] for g in groups]
            self.assertEqual(actual, expected)
            for group in groups:
                self.assertEqual(group['lessons'][-1]['kind'], 'garden')

    def test_textbook_totals(self):
        reading, writing = items('reading'), items('writing')
        self.assertEqual(len(reading), 284)
        self.assertEqual(len({i['char'] for i in reading}), 280)
        self.assertEqual(len(writing), 100)
        self.assertEqual(len({i['char'] for i in writing}), 100)
        self.assertEqual(len([i for i in reading if not i.get('additionalPronunciation')]), 280)

    def test_original_multiple_readings_and_neutral_tones(self):
        reading = items('reading')
        marked = [(i['char'], i['pinyin']) for i in reading if i.get('additionalPronunciation')]
        self.assertEqual(marked, [('地', 'de'), ('着', 'zháo'), ('数', 'shǔ'), ('长', 'zhǎng')])
        for char, sounds in {'地': ['dì', 'de'], '数': ['shù', 'shǔ'], '着': ['zhe', 'zháo'], '长': ['cháng', 'zhǎng'], '谁': ['shuí'], '了': ['le'], '的': ['de'], '们': ['men'], '么': ['me'], '爪': ['zhuǎ']}.items():
            self.assertEqual([i['pinyin'] for i in reading if i['char'] == char], sounds)
        self.assertEqual(next(i['pinyin'] for i in items('writing') if i['char'] == '了'), 'le')

    def test_data_is_complete_and_ids_are_unambiguous(self):
        ids = [l['id'] for mode in ['reading', 'writing'] for g in DATA[mode + 'Groups'] for l in g['lessons']]
        self.assertEqual(len(ids), len(set(ids)))
        for item in items('reading') + items('writing'):
            self.assertEqual(len(item['char']), 1)
            self.assertTrue(item['pinyin'])
            self.assertEqual(unicodedata.normalize('NFC', item['pinyin']), item['pinyin'])
        self.assertEqual(set(STROKES), {i['char'] for i in items('reading') + items('writing')})
        for char, data in STROKES.items():
            self.assertTrue(data['strokes'], char)
            self.assertEqual(len(data['strokes']), len(data['medians']), char)
            for stroke, median in zip(data['strokes'], data['medians']):
                self.assertTrue(stroke.startswith('M'), char)
                self.assertGreaterEqual(len(median), 2, char)


if __name__ == '__main__':
    unittest.main()
