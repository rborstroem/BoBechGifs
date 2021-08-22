import scroller
import id_scraper


scroller.scroll()

# Remove duplicates in file
with open("ids.txt", "r") as f:
    num = 0
    all_ids = f.read().split(", ")

unique_ids = set(all_ids)

for x in unique_ids:
    num += 1

print(num)

with open("unique_ids.csv", "w") as f:
    for id in unique_ids:
        f.write(id + ", ")
