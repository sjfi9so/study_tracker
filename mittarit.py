import json
from pathlib import Path
TIEDOSTO_POLKU = Path(__file__).parent / "sessions.json"


def keskiarvo(minutes, sessarit):
    keskiminuutit = minutes / sessarit
    tunti = int(keskiminuutit // 60)
    minuutti = round(keskiminuutit % 60)
    return f"{tunti}h {minuutti}min"


def minutes_hours(minutes):
    tunnit = (minutes // 60)
    minuutit = (minutes % 60)
    return f"{tunnit}h {minuutit}min"


def arvonviivytys(kokonaisluku, minimi=1):
    while True:
        try:
            arvo = int(input(kokonaisluku))
            if arvo < minimi:
                print(f"arvon pitää ylittää numero {minimi}")
                continue
            return arvo
        except ValueError:
            print("virheellinen syöte, syötä kokonaisluku esim. 32")


def katso():
    try:
        with open(TIEDOSTO_POLKU, "r", encoding="utf-8") as f:
            return json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


sessions = katso()
while True:
    print()
    print("1. lisää session")
    print("2. näytä kaikki sessionit")
    print("3. näytä kokonaisopiskeluaika")
    print("4. näytä avg opiskeluaika")
    print("5. quit")
    print("6. poista kohde")

    choice = input("choose: ")
    if choice == "1":
        aine = input("aine: ").strip()
        if not aine:
            print("et voi palauttaa tyhjää")
            continue

        minutes = arvonviivytys("lisää minuutit", minimi=1)
        session = {"aine": aine, "minutes": minutes}
        sessions.append(session)

        with open(TIEDOSTO_POLKU, "w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=4, ensure_ascii=False)

    elif choice == "2":
        print("\n--- sessions ---")
        for s in sessions:
            print(f"aine: {s['aine']}, minutes: {s['minutes']}")

    elif choice == "3":
        yhteensa = 0
        for s in sessions:
            yhteensa += s["minutes"]
        print(f"kokonaisopiskeluaika {minutes_hours(yhteensa)}")

    elif choice == "4":
        if len(sessions) > 0:
            yhteensa = 0
            for s in sessions:
                yhteensa += s["minutes"]

            AVGopiskeluaika = keskiarvo(yhteensa, len(sessions))
            print(f"KeskiKoodausAika Päivässä {AVGopiskeluaika}")

    elif choice == "5":
        print("valmista boiii")
        break

    elif choice == "6":
        for i, s in enumerate(sessions):
            print(f"{i + 1} aine: {s['aine']}, minutes: {s['minutes']}")

        valinta = arvonviivytys("valitse poistettava kohde", minimi=1)
        valinta -= 1
        if 0 <= valinta < len(sessions):

            sessions.pop(valinta)
            with open(TIEDOSTO_POLKU, "w", encoding="utf-8") as f:
                json.dump(sessions, f, indent=4, ensure_ascii=False)
                print("poisto onnistui")
        else:
            print("asetit väärän arvon")
