# transform cam676 data sets to chinese

import json
# from baidu_translator.py import baidu_translator
import baidu_translator

def get_result(path):
    with open(path) as f:
        data_set = json.load(f)
    s = set()
    result = []
    no_label = []

    # for count
    count = 0    # the number of total turns
    count_thanks_bye = 0  # the number of turn which act is thanks or bye
    slot_set = set()
    act_set = set()

    for i in range(len(data_set)):
        episode_data = data_set[i]
        for j in range(len(episode_data['dial'])):
            count += 1
            turn_data = episode_data['dial'][j]
            nl_en = turn_data['usr']['transcript']
            slu = turn_data['usr']['slu']
            nl_ch = baidu_translator.baidu_translator(nl_en)
            s_cache = s.copy()
            s.clear()
            turn_result = {}
            no_label_1 = ['', '', [], []]
            for k in range(len(slu)):
                if len(slu[k]['slots']) > 1:
                    print('slu length > 1', 'episode', episode_data['dialogue_id'], 'turn', turn_data['turn'])
                # tup = (act, slot, value)
                if slu[k]['act'] == 'inform':
                    tup = (slu[k]['act'], slu[k]['slots'][0][0], baidu_translator.baidu_translator(slu[k]['slots'][0][1]))
                elif slu[k]['act'] == 'request':
                    tup = (slu[k]['act'], slu[k]['slots'][0][1], None)
                else:
                    print('There is another act!!', slu[k]['act'])
                s.add(tup)
                act_set.add(tup[0])
                slot_set.add(tup[1])
                del tup
            cur_s = s.difference(s_cache)
            if cur_s == set():
                cur_s = thanks_bye(nl_ch)
                count_thanks_bye += 1
            turn_result['nl_en'] = nl_en
            turn_result['nl_ch'] = nl_ch
            turn_result['label_seq'], flag = get_label(nl_ch, cur_s)
            # turn_result['act'] = act
            if cur_s == set():
                # print('no add cur_s!!', 'episode', episode_data['dialogue_id'], 'turn', turn_data['turn'])
                no_label_1[0] = nl_ch
                no_label_1[1] = nl_en
                no_label_1[2] = turn_result['label_seq']
                no_label_1[3] = slu
                no_label.append(no_label_1)
            elif flag == 0:
                result.append(turn_result)
    print('total:', count, '\t', 'count_thanks_bye:', count_thanks_bye, '\n')
    print('act_set:', act_set)
    print('slot_set:', slot_set)
    return result, no_label

def thanks_bye(nl_ch):
    s1 = '谢谢'
    s2 = '再见'
    s = set()
    if nl_ch.find(s1):
        tup = ('thanks', 'thanks', None)
        s.add(tup)
    elif nl_ch.find(s2):
        tup = ('bye', 'bye', None)
        s.add(tup)
    else:
        s = set()
    return s

def get_label(nl_ch, s):
    seq = ['O']*len(nl_ch)
    flag = 0
    for tup in s:
        if tup[2] != None:
            ref = tup[2]
        else:
            ref = baidu_translator.baidu_translator(tup[1])
            # continue
        start_index = nl_ch.find(ref)
        end_index = start_index + len(ref)
        if start_index == -1:
            print('Not find in chinese sequence!!!')
            flag = 1
            # with open('no_match', 'a') as f:
            #     f.write(nl_ch+'\n')
            #     f.write(ref+' '+str(tup)+'\n')
        else:
            seq[start_index] = 'B-'+tup[1]
            seq[start_index+1:end_index] = ['I-'+tup[1]]*(len(ref)-1)
    return seq, flag

'''
if __name__ == '__main__':
    file_path = 'CamRest676.json'
    s, no_label = get_result(file_path)
    print('usable:', len(s), '\t', 'no label', len(no_label))
    with open('data_for_nlu.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(s, ensure_ascii=False))
    for i in range(len(s)):
        seq_in = s[i]['nl_ch']
        seq_out = s[i]['label_seq']
        with open('seq.in', 'a') as f:
            f.write(seq_in+'\n')
        with open('seq.out', 'a') as f:
            for i in range(len(seq_out)):
                f.write(seq_out[i]+' ')
            f.write('\n')
            '''
