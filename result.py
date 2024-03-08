import re
import csv
import sys

# 1. ライブチャレンジの結果を ctrl + A と ctrl + C で全てコピー
# 2. 〇〇.txtというファイルにペースト
# 3. 同じフォルダにあるこの"result.py" を terminalで以下のように打ってEnter 
#```
#python3 result.py 〇〇.txt
#```
# 4. 〇〇.csvが完成
def parse_section(section):
    lines = section.strip().split('\n')
    name = lines[0]
    # print(name)
    pts = []
    distance = []
    time = []
    totals = {}
    for line in lines[1:]:
        pts_match = re.search(r'([\d,]+) pts', line)
        km_match = re.search(r'([\d.]+) km|([\d.]+) m', line)
        time_match = re.search(r'(\d+ min(?:, \d+ sec)?)|\d+ sec', line)
        if pts_match:
            if len(pts) < 5:
                pts.append(int(pts_match.group(1).replace(",","")))
            else:
                totals["pts"] = int(pts_match.group(1).replace(",",""))
        if km_match:
            if km_match.group(1):
                # print(f"{km_match}={km_match.group(0)}")
                km = float(km_match.group(0).replace(",","").split(' ')[0])
                if len(distance) < 5:
                    distance.append(f"{km} km")
                else:
                    totals["distance"] = f"{km} km"
                # print(f"{km} km")
            if km_match.group(2):
                # print(f"{km_match}={km_match.group(0)}")
                m = float(km_match.group(0).replace(",","").split(' ')[0])
                if len(distance) < 5:
                    distance.append(f"{m} m")
                else:
                    totals["distance"] = f"{m} m"
                # print(f"{m} m")
        if time_match:
            if len(time) < 5:
                time.append(time_match.group(0))
            else:
                totals["time"] = time_match.group(0)
    data = {"totals": totals, "pts": pts, "distance": distance, "time": time}
    return name, data

def main():
    args = sys.argv
    input_file_name = args[1]
    with open('result.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    total_index = content.find('Round 3\nRound 4\nRound 5\nTotal')
    if total_index != -1:
        content = content[total_index:]

    challenge_index = content.find('CHALLENGE A FRIEND\n\nFRIENDS')
    if challenge_index != -1:
        content = content[:challenge_index]
    sections = re.split(r'\d+\.\n', content)
    results = {}

    for section in sections[1:]:
        name, data = parse_section(section)
        results[name] = data
    # print(results)

# CSVファイルに書き込む
    with open(f'{input_file_name.split(".")[0]}.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Total_Points', 'Total_Distance', 'Total_Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, details in results.items():
            writer.writerow({
                'Name': name,
                'Total_Points': details['totals']['pts'],
                'Total_Distance': details['totals']['distance'],
                'Total_Time': details['totals']['time']
            })

if __name__ == "__main__":
    main()
