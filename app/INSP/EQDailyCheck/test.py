from config import DAILY_ITEM_DICT

itemList = []
for AREA in DAILY_ITEM_DICT:
    for LINE in DAILY_ITEM_DICT[AREA]:
        for EQ in DAILY_ITEM_DICT[AREA][LINE]:
            for ITEM in DAILY_ITEM_DICT[AREA][LINE][EQ]:
                itemList.append(EQ + "_" + ITEM)
print(itemList)