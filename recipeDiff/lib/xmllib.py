import xml.etree.ElementTree as ET
def getXML(n):
    tree = ET.parse("xmldata/"+n)
    root = tree.getroot()

    data = []

    for apartment in root:
        for group in apartment:
            tmpGroup = {}
            tmpGroup["name"] = group.attrib
            tmpGroup["recipes"] = []
            for recipe in group.findall("Recipe"):
                tmpRecipe = {}
                tmpRecipe["name"] = str(recipe.attrib)
                end = tmpRecipe['name'].find('}')
                tmpRecipe["name"] =tmpRecipe['name'][16:end-1]
                tmpRecipe["vars"] = []
                for value in recipe.findall("RecipeValue"):
                    tmpRecipe["vars"].append(value.attrib)
                tmpGroup["recipes"].append(tmpRecipe)
            data.append(tmpGroup)

    return data
