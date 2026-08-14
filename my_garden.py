import os
import json
import random
import time

SAVE_FILE = "save.json"

player_data = {
            "next_id": 1,
            "Инвентарь": {
                "Семена": [],
                "Собраные растения": []
            },
            "Деньги": 20,
            "Огород": {
                "грядка_1": None,
                "грядка_2": None,
                "грядка_3": None,
                "грядка_4": None,
                "грядка_5": None,
                "грядка_6": None,
                "грядка_7": None,
                "грядка_8": None,                                                     
                "грядка_9": None
            }
        }

plants_data = {
        "Морковь" : {
            "seed_price": 12,
            "min_weight": 100,
            "max_weight": 240,
            "ripening_time": 50,
            "price_per_gram": 0.1
            },
        "Помидор" : {
            "seed_price": 8,
            "min_weight": 70,
            "max_weight": 140,
            "ripening_time": 30,
            "price_per_gram": 0.1
            },
        "Арбуз" : {
            "seed_price": 16,
            "min_weight": 900,
            "max_weight": 2300,
            "ripening_time": 90,
            "price_per_gram": 0.05
            },
        "Огурец" : {
            "seed_price": 10,
            "min_weight": 90,
            "max_weight": 160,
            "ripening_time": 40,
            "price_per_gram": 0.1
            }

}


def save_data():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(player_data, f, indent=4, ensure_ascii=False)

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
def buy_seeds(plant_name):
    if plant_name not in plants_data:
        print("Такого растения нет!")
        return
    
    price = plants_data[plant_name]["seed_price"]
    if player_data["Деньги"] >= price:
        player_data["Деньги"] -= price
        seed = {"name": plant_name, "id": get_new_id()}
        player_data["Инвентарь"]["Семена"].append(seed)
        print(f"Куплены семена {plant_name} (ID: {seed['id']})!")
        save_data()  
    else:
        print(f"Не хватает денег! Нужно {price}, у вас {player_data['Деньги']}")
def seeds_shop():
    while True:
        print("Магазин семян:")
        plants = list(plants_data.items())
        for i, (name, data) in enumerate(plants, 1):
            print(f"{i}. {name} — {data['seed_price']} монет")
    
        try:
            choice = int(input("Выберите номер растения для покупки (0 - выход): "))
            if choice == 0:
                break
            if 1 <= choice <= len(plants):
                plant_name = plants[choice-1][0]
                buy_seeds(plant_name)
            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите число!")
def get_new_id():
    global player_data
    new_id = player_data["next_id"]
    player_data["next_id"] += 1
    return new_id

def plant_seed():
    while True:
        seeds = player_data["Инвентарь"]["Семена"]
        if not seeds:
            print("У вас нет семян!")
            return
        
        
        free_beds = [bed_id for bed_id, bed in player_data["Огород"].items() if bed is None]
        if not free_beds:
            print("Нет свободных грядок!")
            return
        
        print("Ваши семена:")
        for i, seed in enumerate(seeds, 1):
            print(f"{i}. {seed['name']} (ID: {seed['id']})")
        
        try:
            choice = int(input("Выберите номер семени для посадки (0 - выход): "))
            if choice == 0:
                return
            if 1 <= choice <= len(seeds):
                seed = seeds[choice-1]
                plant_name = seed["name"]
                
                for bed_id, bed in player_data["Огород"].items():
                    if bed is None:
                        player_data["Огород"][bed_id] = {
                            "plant": plant_name,
                            "planted_at": time.time(),
                            "ready": False
                        }
                        seeds.remove(seed)
                        print(f"{plant_name} посажена на {bed_id}!")
                        break
            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите число!")
def garden():
    for bed_id, bed in player_data["Огород"].items():
        if bed is not None and not bed.get("ready", False):
            plant_name = bed["plant"]
            planted_at = bed["planted_at"]
            ripening_time = plants_data[plant_name]["ripening_time"]
            if time.time() - planted_at >= ripening_time:
                bed["ready"] = True
            save_data()
def harvest():
    while True:
        garden()
    
        ready_beds = []
        for bed_id, bed in player_data["Огород"].items():
            if bed is not None and bed.get("ready", False):
                ready_beds.append(bed_id)
    
        if not ready_beds:
            print("Нет созревших растений для сбора!")
            return
    
        print("Созревшие грядки:")
        for i, bed_id in enumerate(ready_beds, 1):
            plant_name = player_data["Огород"][bed_id]["plant"]
            print(f"{i}. {bed_id}: {plant_name}")
    
        try:
            choice = int(input("Выберите номер грядки для сбора (0 - отмена): "))
            if choice == 0:
                break
            if 1 <= choice <= len(ready_beds):
                bed_id = ready_beds[choice-1]
                bed = player_data["Огород"][bed_id]
                plant_name = bed["plant"]
                weight = random.randint(plants_data[plant_name]["min_weight"], plants_data[plant_name]["max_weight"])
            
                harvested = {
                    "name": plant_name,
                    "weight": weight,
                    "id": get_new_id()
                }
                
                player_data["Инвентарь"]["Собраные растения"].append(harvested)
                player_data["Огород"][bed_id] = None
                print(f"Собрано {plant_name} весом {weight} г!")
                save_data()

            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите число!")
def sell_plant():
    while True:
        harvest_list = player_data["Инвентарь"]["Собраные растения"]
    
        if not harvest_list:
            print("У вас нет собранных растений для продажи!")
            return
    
        print("Ваши собранные растения:")
        for i, plant in enumerate(harvest_list, 1):
            print(f"{i}. {plant['name']} (вес: {plant['weight']} г, ID: {plant['id']})")
    
        try:
            choice = int(input("Выберите номер растения для продажи (0 - отмена): "))
            if choice == 0:
                break
            if 1 <= choice <= len(harvest_list):
                plant = harvest_list[choice-1]
                price = plant["weight"] * plants_data[plant["name"]]["price_per_gram"]
                player_data["Деньги"] += price
                harvest_list.remove(plant)
                print(f"Продано {plant['name']} за {price:.2f} монет!")
            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите число!")
        save_data()

def inventory():
    harvest_list = player_data["Инвентарь"]["Собраные растения"]
    seeds = player_data["Инвентарь"]["Семена"]
    money = player_data["Деньги"]
    print(f"У вас {money}$")
    if not harvest_list:
        print("У вас нет собраных растений!")
    else:
        print(f"Ваши собраные растения:")
        for i, plant in enumerate(harvest_list, 1):
            print(f"{plant['name']} (вес: {plant['weight']} г, ID: {plant['id']})")
    if not seeds:
        print("У вас нет семян!")
    else:
        print(f"Ваши семена:")
        for i, seed in enumerate(seeds, 1):
            print(f"{seed['name']} (ID: {seed['id']})")
    input("Нажмите Enter, чтобы вернуться...")

def show_garden():
    print("Ваш огород:")
    for bed_id, bed in player_data["Огород"].items():
        if bed is None:
            print(f"   {bed_id}: пусто")
        else:
            plant_name = bed["plant"]
            status = "✅ ГОТОВО" if bed.get("ready") else " растёт..."
            print(f"   {bed_id}: {plant_name} {status}")
    input("Нажмите Enter, чтобы вернуться...")

loaded = load_data()
if loaded:
    player_data = loaded
else:
    player_data = {
            "next_id": 1,
            "Инвентарь": {"Семена": [], "Собраные растения": []},
            "Деньги": 20,
            "Огород": {f"грядка_{i}": None for i in range(1, 10)}
                    }
save_data()  
                
while True:   
    garden()
    print("1. Магазин")
    print("2. Посадка семян")
    print("3. Сбор урожая")
    print("4. Продажа растений")
    print("5. Огород")
    print("6. Инвентарь")
    print("Для выхода напишите '0'")
    x = input(">")
    if x == "1":
        seeds_shop()
    elif x == "2":
        plant_seed()
    elif x == "3":
        harvest()
    elif x == "4":
        sell_plant()
    elif x == "5":
        show_garden()
    elif x == "6":
        inventory()
    elif x == "0":
        save_data()
        break
    else:
        print("Неверный команда!")

