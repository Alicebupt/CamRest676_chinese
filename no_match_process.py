# encoding: utf-8

import json
import linecache
import baidu_translator

def get_label(nl_ch, s, value):
    seq = ['O']*len(nl_ch)
    flag = 0
    for tup in s:
        if tup[2] != 'None':
            ref = tup[2]
        else:
            ref = value
            # continue
        start_index = nl_ch.find(ref)
        end_index = start_index + len(ref)
        if start_index == -1:
            print('Not find in chinese sequence!!!')
            flag = 1
            act = tup[0]
            path = 'no_match'
            with open(path, 'a') as f:
                f.write(nl_ch)
                f.write(ref+' '+str(tup)+'\n')
        else:
            seq[start_index] = 'B-'+tup[1]
            seq[start_index+1:end_index] = ['I-'+tup[1]]*(len(ref)-1)
    return seq, flag

def get_usable_data(path):

    usable_data = []
    for i in range(1, 162):
        data = linecache.getline(path, i)
        turn_result = {}
        cur_s = set()
        cur_list = []
        if i %2 == 1:
            nl = data
        else:
            data = data.split()
            for j in range(len(data)):
                data[j] = data[j].strip('(),\'')
            # print(data)
            act = data[1]
            slot = data[2]
            value = data[3]
            value1 = baidu_translator.baidu_translator(slot)
            if act != 'thanks':
                if value1 == '地址':
                    # if value[2] == '的':
                    value1 = '在哪里'
                tup = (act, slot, value)
                cur_s.add(tup)
                cur_list.append(tup)
                seq, flag = get_label(nl, cur_s, value1)
                if flag == 0:
                    turn_result['nl_ch'] = nl
                    turn_result['label_seq'] = seq
                    turn_result['act'] = cur_list
                    usable_data.append(turn_result)
    print('len(usable_data):', len(usable_data))
    return usable_data



if __name__ == '__main__':
    path = 'requestno_match'
    usable_data = get_usable_data((path))
    with open('usable.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(usable_data, ensure_ascii=False))
