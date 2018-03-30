class HierarchicalModel:
    def __init__(self):
        self.connection = dict()
        self.dirDict = dict()
        self.unmatched = []

    def add(self, id, parentId=None, item=None):
        self.dirDict[id] = item
        self.connection[id] = []

        found = False

        if parentId is not None:
            for k in self.connection:
                if k == parentId :
                    self.connection[k].append(id)
                    found = True
                    break

            if not found:
                self.unmatched.append(id)

        if self.unmatched:
            for i in self.unmatched[::]:
                if id == self.dirDict[i].parentId:
                    self.connection[id].append(i)
                    self.unmatched.remove(i)

    def getTree(self, rootId):
        return self.dirDict[rootId], [ self.getTree(i) for i in self.connection[rootId] ]

    def getChildrenOf(self, parentId, getIdOnly=False):
        if getIdOnly :
            return self.connection[parentId][::]

        return [ self.dirDict[i] for i in self.connection[parentId] ]

    def parentOf(self, childId):
        for parent, childList in self.connection.items() :
            if childId in childList :
                return parent

        return None

    def hasParent(self, childId):
        return self.parentOf(childId) is not None

    def removeById(self, id):
        if id not in self.dirDict :
            return

        self.dirDict.pop(id)
        for parent, childList in self.connection.items() :
            if id in childList :
                childList.remove(id)

    def getIds(self):
        return self.dirDict.keys()

    def hasChildren(self, id):
        return self.connection[id]

    def getDir(self, id):
        return self.dirDict[id]

    def getNameOf(self, id):
        try: return self.dirDict[id].name
        except: pass

        try: return self.dirDict[id]['name']
        except: pass

        return str(self.dirDict[id])


if __name__ == '__main__' :
    tree = HierarchicalModel()
    tree.add(0, item="root")
    tree.add(1, 0, item="3D models")
    tree.add(2, 1, item="Weapons")
    tree.add(3, 2, item="Guns")
    tree.add(4, 2, item="Melees")
    tree.add(5, 2, item="Bombs")
    tree.add(6, 1, item="Vehicles")
    tree.add(7, 6, item="Boats")
    tree.add(8, 6, item="Bikes")
    tree.add(9, 1, item="Trees")
    tree.add(10, 0, item="Sprite Sheets")
    tree.add(11, 10, item="Characters")
    tree.add(12, 10, item="Effects")

    print(tree.connection)
    print(tree.getTree(0))