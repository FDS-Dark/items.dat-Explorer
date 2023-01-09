import struct
import os
import glob
import shutil
import subprocess
import shlex
from PIL import Image

#VARIABLES
SECRET = "PBG892FXX982ABC*"
GT = os.getenv('LOCALAPPDATA') + '\\Growtopia'
itemsDat = GT + '\\cache\\items.dat'

#Item Dictionaries
masterItemDict = []

class bcolors:
    RESET = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def memcpy(id, nlen, pos, enc, data):
    str = ''
    if enc == True:
        for i in range(nlen):
            str += chr(data[pos])
            pos += 1
    else:
        for i in range(nlen):
            str += chr(data[pos] ^ ord(SECRET[(id + i) % len(SECRET)]))
            pos += 1
    return str

def decFile(data):
    memPos = 0
    itemsdatVersion = struct.unpack('<H', data[memPos:memPos+2])[0]
    memPos += 2
    itemCount = struct.unpack('i', data[memPos:memPos+4])[0]
    memPos += 4
    for i in range(itemCount):
        itemDict = {}

        itemID = struct.unpack('i', data[memPos:memPos+4])[0]
        itemDict['itemID'] = itemID

        memPos += 4
        
        editableType = data[memPos]
        memPos += 1
        itemCategory = data[memPos]
        memPos += 1
        actionType = data[memPos]
        memPos += 1
        hitSoundType = data[memPos]
        memPos += 1
        
        ##name parse
        strLen = data[memPos] + data[memPos + 1] * 256
        
        memPos += 2
        name = memcpy(itemID,strLen,memPos, False, data)
        memPos += strLen
        ##name parse end
        
        ##texture parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        texture = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##texture parse
        
        #texturehash parse
        textureHash = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #itemKind
        itemKind = data[memPos]
        memPos += 1
        #end
        
        #val1 parse
        val1 = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #textureX & textureY
        textureX = data[memPos]
        memPos += 1

        textureY = data[memPos]
        memPos += 1
        #end
        
        #spreadType
        spreadType = data[memPos]
        memPos += 1
        #end
        
        #stripeywallpaper
        isStripeyWallpaper = data[memPos]
        memPos += 1
        #end
        
        #Collision
        collisionType = data[memPos]
        memPos += 1
        #end
        
        #breakHits
        breakHits = data[memPos]
        memPos += 1
        #end
        
        #dropChance
        dropChance = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #clothingType 
        clothingType = data[memPos]
        memPos += 1
        #end
        
        #rarity
        rarity = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        #end
        
        #maxAmount
        maxAmount = data[memPos]
        memPos += 1
        #end
        
        ##extrFile parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraFile = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##extraFile parse
        
        #extraFilehash
        extraFilehash = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #audioVolume
        audioVolume = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        ##pet option
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petName = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petPrefix = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petSuffix = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petAbility = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##pet option
        
        #seed(base,overlay)
        seedBase = data[memPos]
        seedOverlay = data[memPos]
        memPos += 2
        #end
        
        #tree(base,leaves)
        treeLeaves = data[memPos]
        treeBase = data[memPos]
        memPos += 2
        #end
        
        #seed(color,overlaycolor)
        seedColor = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        seedOverlayColor = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        memPos += 4 #deleted ingridients
        
        #growTime
        growTime = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #val2 & isRayman
        val2 = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        isRayman = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        #end
        
        ##item extra data
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraOptions = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        texture2 = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraOptions2 = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        ##item extra data
        
        memPos += 80; #unknown data
        
        if (itemsdatVersion >= 11):
            strLen = data[memPos] + data[memPos + 1] * 256
            memPos += 2
            punchOptions = memcpy(itemID,strLen,memPos, True, data)
            memPos += strLen
            
            if (itemsdatVersion >= 12):
                memPos += 13
        
        if (itemsdatVersion >= 13):
            memPos += 4
        
        if  (itemsdatVersion >= 14):
            memPos += 4 # skip data
      
        if i != itemID:
            print('Unordered item ' + str(itemID) + '/' + str(itemCount))

        itemDict['name'] = name.lower()
        itemDict['nameWithCaps'] = name
        itemDict['itemID'] = itemID
        itemDict['editableType'] = editableType
        itemDict['itemCategory'] = itemCategory
        itemDict['actionType'] = actionType
        itemDict['hitSoundType'] = hitSoundType
        itemDict['texture'] = texture
        itemDict['textureHash'] = textureHash
        itemDict['itemKind'] = itemKind
        itemDict['val1'] = val1
        itemDict['textureX'] = textureX
        itemDict['textureY'] = textureY
        itemDict['spreadType'] = spreadType
        itemDict['isStripeyWallpaper'] = isStripeyWallpaper
        itemDict['collisionType'] = collisionType
        itemDict['breakHits'] = breakHits
        itemDict['dropChance'] = dropChance
        itemDict['clothingType'] = clothingType
        itemDict['rarity'] = rarity
        itemDict['maxAmount'] = maxAmount
        itemDict['extraFile'] = extraFile
        itemDict['extraFilehash'] = extraFilehash
        itemDict['audioVolume'] = audioVolume
        itemDict['petName'] = petName
        itemDict['petPrefix'] = petPrefix
        itemDict['petSuffix'] = petSuffix
        itemDict['petAbility'] = petAbility
        itemDict['seedBase'] = seedBase
        itemDict['seedOverlay'] = seedOverlay
        itemDict['treeLeaves'] = treeLeaves
        itemDict['treeBase'] = treeBase
        itemDict['seedColor'] = seedColor
        itemDict['seedOverlayColor'] = seedOverlayColor
        itemDict['growTime'] = growTime
        itemDict['val2'] = val2
        itemDict['isRayman'] = isRayman
        itemDict['extraOptions'] = extraOptions
        itemDict['texture2'] = texture2
        itemDict['extraOptions2'] = extraOptions2
        itemDict['punchOptions'] = punchOptions

        masterItemDict.append(itemDict)
        return data #Developer use
    
def decFileNames(data):
    names = []
    memPos = 0
    itemsdatVersion = struct.unpack('<H', data[memPos:memPos+2])[0]
    memPos += 2
    itemCount = struct.unpack('i', data[memPos:memPos+4])[0]
    memPos += 4
    for i in range(itemCount):
        itemDict = {}

        itemID = struct.unpack('i', data[memPos:memPos+4])[0]
        itemDict['itemID'] = itemID

        memPos += 4
        
        editableType = data[memPos]
        memPos += 1
        itemCategory = data[memPos]
        memPos += 1
        actionType = data[memPos]
        memPos += 1
        hitSoundType = data[memPos]
        memPos += 1
        
        ##name parse
        strLen = data[memPos] + data[memPos + 1] * 256
        
        memPos += 2
        name = memcpy(itemID,strLen,memPos, False, data)
        memPos += strLen
        ##name parse end
        
        ##texture parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        texture = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##texture parse
        
        #texturehash parse
        textureHash = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #itemKind
        itemKind = data[memPos]
        memPos += 1
        #end
        
        #val1 parse
        val1 = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #textureX & textureY
        textureX = data[memPos]
        memPos += 1

        textureY = data[memPos]
        memPos += 1
        #end
        
        #spreadType
        spreadType = data[memPos]
        memPos += 1
        #end
        
        #stripeywallpaper
        isStripeyWallpaper = data[memPos]
        memPos += 1
        #end
        
        #Collision
        collisionType = data[memPos]
        memPos += 1
        #end
        
        #breakHits
        breakHits = data[memPos]
        memPos += 1
        #end
        
        #dropChance
        dropChance = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #clothingType 
        clothingType = data[memPos]
        memPos += 1
        #end
        
        #rarity
        rarity = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        #end
        
        #maxAmount
        maxAmount = data[memPos]
        memPos += 1
        #end
        
        ##extrFile parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraFile = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##extraFile parse
        
        #extraFilehash
        extraFilehash = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #audioVolume
        audioVolume = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        ##pet option
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petName = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petPrefix = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petSuffix = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petAbility = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##pet option
        
        #seed(base,overlay)
        seedBase = data[memPos]
        seedOverlay = data[memPos]
        memPos += 2
        #end
        
        #tree(base,leaves)
        treeLeaves = data[memPos]
        treeBase = data[memPos]
        memPos += 2
        #end
        
        #seed(color,overlaycolor)
        seedColor = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        seedOverlayColor = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        memPos += 4 #deleted ingridients
        
        #growTime
        growTime = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #val2 & isRayman
        val2 = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        isRayman = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        #end
        
        ##item extra data
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraOptions = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        texture2 = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraOptions2 = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        ##item extra data
        
        memPos += 80; #unknown data
        
        if (itemsdatVersion >= 11):
            strLen = data[memPos] + data[memPos + 1] * 256
            memPos += 2
            punchOptions = memcpy(itemID,strLen,memPos, True, data)
            memPos += strLen
            
            if (itemsdatVersion >= 12):
                memPos += 13
        
        if (itemsdatVersion >= 13):
            memPos += 4
        
        if  (itemsdatVersion >= 14):
            memPos += 4 # skip data
      
        if i != itemID:
            print('Unordered item ' + str(itemID) + '/' + str(itemCount))
        
        names.append(name)
    return names

def reloadItems():
    #Growtopia folder
    game = GT + '\\game\\**\*.rttex'
    gameFiles = glob.glob(game, recursive=True)

    cache = GT + '\\cache\\**\*.rttex'
    cacheFiles = glob.glob(cache, recursive=True)

    for file in gameFiles:
        sprites = os.getcwd() + r"\sprites"
        shutil.copy(file, sprites)
    
    for file in cacheFiles:
        sprites = os.getcwd() + r"\sprites"
        shutil.copy(file, sprites)

def compareItems(old, new):
    oldNames = decFileNames(open(old, 'rb').read())
    newNames = decFileNames(open(new, 'rb').read())

    differences = []

    fileDir = os.getcwd() + r'\output\comparedFiles.txt'

    if os.path.exists(fileDir):
        os.remove(fileDir)

    for element in newNames:
        if element not in oldNames:
            differences.append(element)
    with open(fileDir, 'a') as f:
        f.write("New items:\n")
        for item in differences:
            f.write(item + "\n")
    print("\nYou'll find the differences file in the 'output' directory in the text file 'comparedFiles.txt'")

def checkForFolders():
    curDir = os.getcwd()

    if not os.path.exists(curDir + r'\files'):
        os.mkdir(curDir + r'\files')

    if not os.path.exists(curDir + r'\inputs'):
        os.mkdir(curDir + r'\inputs')

    if not os.path.exists(curDir + r'\output'):
        os.mkdir(curDir + r'\output')

    if not os.path.exists(curDir + r'\temp'):
        os.mkdir(curDir + r'\temp')
        
    if not os.path.exists(curDir + r'\sprites'):
        os.mkdir(curDir + r'\sprites')

    if os.path.exists(curDir + r'\RTPackConverter.exe'):
        shutil.move(curDir + r'\RTPackConverter.exe', curDir + r'\files')

    if os.path.exists(curDir + r'\RTPackConverter.exe.config'):
        shutil.move(curDir + r'\RTPackConverter.exe.config', curDir + r'\files')

    if os.path.exists(curDir + r'\RTPackConverter.pdb'):
        shutil.move(curDir + r'\RTPackConverter.pdb', curDir + r'\files')

def getSpriteFromName(name):
    if isinstance(name, str):
        dictObject = next(item for item in masterItemDict if item["name"] == name.lower())
        textureFile = dictObject['texture']
        textureX = dictObject['textureX']
        textureY = dictObject['textureY']
        nameWithCaps = dictObject['nameWithCaps']

        if 'pets/' in textureFile:
            textureFile = textureFile.replace("pets/", "")
            
        rttextoimage = os.getcwd() + r'\files\RTPackConverter.exe'
        fileDir = os.getcwd() + f"\sprites\{textureFile}"
        
        temp = os.getcwd() + r'\temp'
        shutil.copy(fileDir, temp)
        fileDir = os.getcwd() + r'\temp' + f'\{textureFile}'
        rttexCMD = f'"{rttextoimage}" "{fileDir}"'
        subprocess.run(shlex.split(rttexCMD))

        imgTextureFile = textureFile.replace(".rttex", '.png')
        imgDir = temp + f'\{imgTextureFile}'
        spriteSheet = Image.open(imgDir)

        left = (textureX) * 32
        top = (textureY) * 32
        right = (left + 31)
        bottom = (top + 31)

        croppedImage = spriteSheet.crop((left, top, right, bottom))
        croppedImage.save(os.getcwd() + '\output' + f'\{nameWithCaps}.png')

        rtpackFiles = os.getcwd() + '\\**\*.rtpack'
        rtpackFiles = glob.glob(rtpackFiles, recursive=True)

        for rtpack in rtpackFiles:
            os.remove(rtpack)
        
        tempFilesPNG = os.getcwd() + '\\temp\**\*.png'
        tempFilesPNG = glob.glob(tempFilesPNG, recursive=True)
        tempFilesRTTEX = os.getcwd() + '\\temp\**\*.rttex'
        tempFilesRTTEX = glob.glob(tempFilesRTTEX, recursive=True)


        for png in tempFilesPNG:
            os.remove(png)

        for rttex in tempFilesRTTEX:
            os.remove(rttex)

    elif isinstance(name, list):
        spriteItemNames = []
        for itemName in name:
            spriteItemNames.append(next(item for item in masterItemDict if item["name"] == itemName.lower()))

        for dictObject in spriteItemNames:
            textureFile = dictObject['texture']
            textureX = dictObject['textureX']
            textureY = dictObject['textureY']
            itemName = dictObject['name']
            nameWithCaps = dictObject['nameWithCaps']

            rttextoimage = os.getcwd() + r'\files\RTPackConverter.exe'
            fileDir = os.getcwd() + f"\sprites\{textureFile}"
            
            temp = os.getcwd() + r'\temp'
            shutil.copy(fileDir, temp)
            fileDir = os.getcwd() + r'\temp' + f'\{textureFile}'
            rttexCMD = f'"{rttextoimage}" "{fileDir}"'
            subprocess.run(shlex.split(rttexCMD))
    
            imgTextureFile = textureFile.replace(".rttex", '.png')
            imgDir = temp + f'\{imgTextureFile}'
            spriteSheet = Image.open(imgDir)
    
            left = (textureX) * 32
            top = (textureY) * 32
            right = (left + 31)
            bottom = (top + 31)
    
            croppedImage = spriteSheet.crop((left, top, right, bottom))
            croppedImage.save(os.getcwd() + '\output' + f'\{nameWithCaps}.png')
            rtpackFiles = os.getcwd() + '\\**\*.rtpack'
            rtpackFiles = glob.glob(rtpackFiles, recursive=True)

            for rtpack in rtpackFiles:
                os.remove(rtpack)
            
            if os.path.exists(fileDir):
                os.remove(fileDir)

            if os.path.exists(imgDir):
                os.remove(imgDir)
    
def generateList(dictObject):
    itemName = dictObject['name']
    nameWithCaps = dictObject['nameWithCaps']
    itemID = dictObject['itemID']
    editableType = dictObject['editableType']
    itemCategory = dictObject['itemCategory']
    actionType = dictObject['actionType']
    hitSoundType = dictObject['hitSoundType']
    texture = dictObject['texture']
    textureHash = dictObject['textureHash']
    itemKind = dictObject['itemKind']
    val1 = dictObject['val1']
    textureX = dictObject['textureX']
    textureY = dictObject['textureY']
    spreadType = dictObject['spreadType']
    isStripeyWallpaper = dictObject['isStripeyWallpaper']
    collisionType = dictObject['collisionType']
    breakHits = dictObject['breakHits']
    dropChance = dictObject['dropChance']
    clothingType = dictObject['clothingType']
    rarity = dictObject['rarity']
    maxAmount = dictObject['maxAmount']
    extraFile = dictObject['extraFile']
    extraFilehash = dictObject['extraFilehash']
    audioVolume = dictObject['audioVolume']
    petName = dictObject['petName']
    petPrefix = dictObject['petPrefix']
    petSuffix = dictObject['petSuffix']
    petAbility = dictObject['petAbility']
    seedBase = dictObject['seedBase']
    seedOverlay = dictObject['seedOverlay']
    treeLeaves = dictObject['treeLeaves']
    treeBase = dictObject['treeBase']
    seedColor = dictObject['seedColor']
    seedOverlayColor = dictObject['seedOverlayColor']
    growTime = dictObject['growTime']
    val2 = dictObject['val2']
    isRayman = dictObject['isRayman']
    extraOptions = dictObject['extraOptions']
    texture2 = dictObject['texture2']
    extraOptions2 = dictObject['extraOptions2']
    punchOptions = dictObject['punchOptions']

    message = f'itemName: {nameWithCaps}' + '\n' + f'itemID: {itemID}' + '\n' + f'editableType: {editableType}' + '\n' + f'itemCategory: {itemCategory}' + '\n' + f'actionType: {actionType}' + '\n' + f'hitSoundtype: {hitSoundType}' + '\n' + f'texture: {texture}' + '\n' + f'textureHash: {textureHash}' + '\n' + f'itemKind: {itemKind}' + '\n' + f'val1: {val1}' + '\n' + f'textureX: {textureX}' + '\n' + f'textureY: {textureY}' + '\n' + f'spreadType: {spreadType}' + '\n' + f'isStripeyWallpaper: {isStripeyWallpaper}' + '\n' + f'collisionType: {collisionType}' + '\n' + f'breakHits: {breakHits}' + '\n' + f'dropChance: {dropChance}' + '\n' + f'clothingType: {clothingType}' + '\n' + f'rarity: {rarity}' + '\n' + f'maxAmount: {maxAmount}' + '\n' + f'extraFile: {extraFile}' + '\n' + f'extraFileHash: {extraFilehash}' + '\n' + f'audioVolume: {audioVolume}' + '\n' + f'petName: {petName}' + '\n' + f'petPrefix: {petPrefix}' + '\n' + f'petSuffix: {petSuffix}' + '\n' + f'petAbility: {petAbility}' + '\n' + f'seedBase: {seedBase}' + '\n' + f'seedOverlay: {seedOverlay}' + '\n' + f'treeLeaves: {treeLeaves}' + '\n' + f'treeBase: {treeBase}' + '\n' + f'seedColor: {seedColor}' + '\n' + f'seedOverlayColor: {seedOverlayColor}' + '\n' + f'growTime: {growTime}' + '\n' + f'val2: {val2}' + '\n' + f'isRayman: {isRayman}' + '\n' + f'extraOptions: {extraOptions}' + '\n' + f'texture2: {texture2}' + '\n' + f'extraOptions2: {extraOptions2}' + '\n' + f'punchOptions: {punchOptions}' + '\n'

    return message

def getProperties(name):
    if isinstance(name, str):
        dictObject = next(item for item in masterItemDict if item["name"] == name.lower())
        message = generateList(dictObject)

        fileDir = os.getcwd() + r'\output\requestedProperties.txt'
        if os.path.exists(fileDir):
            os.remove(fileDir)

        with open(fileDir, 'a') as f:
            f.write(message)
            f.write('\n')
        print("\nYou'll find your requested properties in the 'output' directory in the text file 'requestedProperties.txt'")


    elif isinstance(name, list):
        spriteItemNames = []
        for itemName in name:
            spriteItemNames.append(next(item for item in masterItemDict if item["name"] == itemName.lower()))

        messages = []
        for dictObject in spriteItemNames:
            dictSummary = generateList(dictObject)
            messages.append(dictSummary)

        fileDir = os.getcwd() + r'\output\requestedProperties.txt'
        if os.path.exists(fileDir):
            os.remove(fileDir)
        with open(fileDir, 'a') as f:
            for item in messages:
                f.write(item)
                f.write('\n')
        print("\nYou'll find your requested properties in the 'output' directory in the text file 'requestedProperties.txt'")

def setup():
    option = input("\nSelect an option below:\n\n[1] Get item sprite from name\n[2] Get item properties from name\n[3] Get list of new items from previous items.dat\n[4] Get sprite sheet from name\n[5] Clear output directory\n[6] Clear temp directory\n")
    global chosen
    chosen = option
    return option

def setupMain(a=None):
    while True:
        if a:
            option = a
        else:
            option = setup()
        
        if option == "1":
            spriteFromNameChoice = input("\nSelect an option below:\n\n[1] Single item\n[2] List of items\n")
            if spriteFromNameChoice == "1":
                itemName = input("\nPlease input the item's name exactly as written.\n")
                getSpriteFromName(itemName)
                break
            elif spriteFromNameChoice == "2":
                itemListStr = input("\nPlease input the items to get the sprite of seperated by commas (ex: Dirt, Bedrock, Golden Angel Wings)\n")
                itemList = itemListStr.split(', ')
                getSpriteFromName(itemList)
                break
            else:
                print("\nInvalid Input!")
        elif option == "2":
            propertyFromName = input("\nSelect an option below:\n\n[1] Single item\n[2] List of items\n")
            if propertyFromName == "1":
                itemName = input("\nPlease input the item's name.\n")
                getProperties(itemName)
                break
            elif propertyFromName == "2":
                itemListStr = input("\nPlease input the items to get the sprite of seperated by commas (ex: Dirt, Bedrock, Golden Angel Wings)\n")
                itemList = itemListStr.split(', ')
                getProperties(itemList)
                break
            else:
                print("\nInvalid Input!")
        elif option == "3":
            itemsPath = os.getcwd() + r'\inputs'
            newItemsList = input("\nPlease place the old and new items.dat files into the 'inputs' directory and type enter anything when done. Files should be labeled 'newitems.dat' and 'olditems.dat'. (You can also type 'current' in order to compare the oldItems.dat to the current items.dat)\n")
            oldItemsDat = os.getcwd() + '\inputs\oldItems.dat'
            newItemsDat = os.getcwd() + '\inputs\\newItems.dat'

            if os.path.exists(oldItemsDat):
                if newItemsList.lower() != "current":
                    if os.path.exists(newItemsDat):
                        compareItems(oldItemsDat, newItemsDat)
                    else:
                        print("\nOne or both of the files are missing! Make sure that the old file is named 'oldItems.dat'!")

                elif newItemsList.lower() == "current":
                    compareItems(oldItemsDat, itemsDat)
            else:
                print("\nOne or both of the files are missing! Make sure the old file is named 'oldItems.dat' and the new one is named 'newItems.dat'!")

        elif option == "4":
            textureFile = input("\nPlease input texture file to convert to png.\n")
            rttextoimage = os.getcwd() + r'\files\RTPackConverter.exe'
            fileDir = os.getcwd() + f"\sprites\{textureFile}"
        
            temp = os.getcwd() + r'\temp'
            shutil.copy(fileDir, temp)

            fileDir = temp + f'\{textureFile}'
            rttexCMD = f'"{rttextoimage}" "{fileDir}"'
            subprocess.run(shlex.split(rttexCMD))
            imgTextureFile = textureFile.replace(".rttex", '.png')
            imgDir = temp + f'\{imgTextureFile}'

            outDir = os.getcwd() + '\output'
            shutil.copy(imgDir, outDir)
            
            rtpackFiles = os.getcwd() + '\\**\*.rtpack'
            rtpackFiles = glob.glob(rtpackFiles, recursive=True)

            for rtpack in rtpackFiles:
                os.remove(rtpack)
            
            if os.path.exists(fileDir):
                os.remove(fileDir)

            if os.path.exists(imgDir):
                os.remove(imgDir)

        elif option == "5":
            outputDir = os.getcwd() + '\output'
            outputPNGs = outputDir + '**\*.png'
            outputPNGs = glob.glob(outputPNGs, recursive=True)

            outputTXTs = outputDir + '**\*.txt'
            outputTXTs = glob.glob(outputTXTs, recursive=True)

            for file in outputPNGs:
                os.remove(file)
            
            for file in outputTXTs:
                os.remove(file)

            break

        elif option == "6":
            outputDirPNG = os.getcwd() + r'\temp\**\*.png'
            outputDirRTTEX = os.getcwd() + r'\temp\**\*.rttex'

            outputFilesPNG = glob.glob(outputDirPNG, recursive=True)
            outputFilesRTTEX = glob.glob(outputDirRTTEX, recursive=True)

            for file in outputFilesPNG:
                os.remove(file)

            for file in outputFilesRTTEX:
                os.remove(file)
            break

        else:
            print("\nInvalid Input!")

logo = """
---------------------------------
  ______ _____   _____ 
 |  ____|  __ \ / ____|
 | |__  | |  | | (___  
 |  __| | |  | |\___ \ 
 | |    | |__| |____) |
 |_|    |_____/|_____/ 

---------------------------------
\n"""

decFile(open(itemsDat, 'rb').read())
checkForFolders()

print(logo + "Welcome to the items.dat Explorer! Created by FDS Dark using code from iFanpS. (Credits to Nenkai / TK69 for the .rttex to .png application)" + "\n")

while True:
    spritesLen = os.listdir(os.getcwd() + r'\sprites')
    if len(spritesLen) == 0:
        print("Loading item sprite files...")
        reloadItems()
        print("Items loaded!")
        break
    else:
        realoadBool = input("Would you like to reload item sprite files? (Y/N)\n")
        if realoadBool.lower() == "y":
            print("\nReloading items! Please wait...")
            reloadItems()
            print("Items reloaded!")
            break
        elif realoadBool.lower() == "n":
            break
        else:
            print("\nInvalid input!")

setupMain()

while True:
    restartBool = input("\nOperation complete! Select an option below\n\n[1] Back to selection\n[2] Re-do last action\n[3] Quit program\n")
    if restartBool == "1":
        setupMain()
    elif restartBool == "2":
        setupMain(chosen)
    elif restartBool == "3":
        quit()
