import AccessoryGlobals, json

# This is the animal that will be added to the accessory globals
mergeAnimal = 'e'

default_hats = AccessoryGlobals.HatTransTable
default_glasses = AccessoryGlobals.GlassesTransTable
hats = AccessoryGlobals.ExtendedHatTransTable
glasses = AccessoryGlobals.ExtendedGlassesTransTable

with open('accessories.json', 'r') as f:
    extra = json.load(f)

def merge(defaultAccessories, specificAccessories, fromDict, type):
    for animal, transform in fromDict['defaults'].items():
        if animal[0] == mergeAnimal:
            defaultAccessories[animal] = tuple([tuple(x) for x in transform])

    for number, specific in fromDict['specific'].items():
        for animal, transform in specific.items():
            if animal[0] == mergeAnimal:
                specificAccessories[int(number)][animal] = tuple([tuple(x) for x in transform])

merge(default_hats, hats, extra['hats'], 'hats')
merge(default_glasses, glasses, extra['glasses'], 'glasses')

def exportSpecific(accessories):
    ids = []

    for number in sorted(accessories.keys()):
        animals = []
        accessory = accessories[number]

        for animal in sorted(accessory.keys()):
            animals.append("        '{0}': {1}".format(animal, accessory[animal]))
        
        id = '    ' + str(number) + ': {\n' + ',\n'.join(animals) + '\n    }'
        ids.append(id)

    return ',\n'.join(ids)

def exportDefault(accessories):
    ids = []
    
    for animal in sorted(accessories.keys()):
        ids.append("    '{0}': {1}".format(animal, accessories[animal]))
    
    return ',\n'.join(ids)

DefaultHatString = exportDefault(default_hats)
DefaultGlassesString = exportDefault(default_glasses)
HatString = exportSpecific(hats)
GlassesString = exportSpecific(glasses)

result = "HatTransTable = {\n" + DefaultHatString + "\n}\nGlassesTransTable = {\n" + DefaultGlassesString + "\n}\nExtendedHatTransTable = {\n" + HatString + "\n}\nExtendedGlassesTransTable = {\n" + GlassesString + "\n}"

with open('AccessoryGlobals_new.py', 'w') as f:
    f.write(result)